import Foundation

/// Builds a `WeeklySnapshot` from stored data for the coaching engine and the
/// optional AI coach. Pure aggregation over the repository.
@MainActor
enum SnapshotBuilder {

    static func build(store: AppStore, profile: UserProfile) -> WeeklySnapshot {
        let cal = Calendar.current
        let now = Date()
        let weekAgo = cal.date(byAdding: .day, value: -7, to: now)!

        // Nutrition averages over logged days in the last week.
        let entries = store.entries(in: weekAgo...now)
        let byDay = Dictionary(grouping: entries, by: { $0.dayKey })
        let loggingDays = byDay.count
        var calSum = 0.0, proSum = 0.0, fibSum = 0.0
        for (_, dayEntries) in byDay {
            let t = NutritionCalculator.totals(dayEntries)
            calSum += t.calories; proSum += t.protein; fibSum += t.fiber
        }
        let denom = Double(max(loggingDays, 1))

        // Steps average over the last week.
        let acts = store.activity(in: weekAgo...now)
        let stepsByDay = Dictionary(grouping: acts.filter { $0.kind == .steps }, by: { $0.dayKey })
        let stepValues = stepsByDay.values.compactMap { $0.first?.steps }
        let avgSteps = stepValues.isEmpty ? 0 : stepValues.reduce(0, +) / stepValues.count

        // Trend slopes from measurements (per week).
        let measurements = store.measurements()
        let weightSlope = weeklySlope(measurements.compactMap { m in m.weightKg.map { (m.date, $0) } })
        let waistSlope = weeklySlope(measurements.compactMap { m in m.waistCm.map { (m.date, $0) } })

        let targets = profile.targets ?? TargetsEngine.compute(for: profile).targets

        return WeeklySnapshot(
            goal: profile.goal,
            bodyWeightKg: profile.currentWeightKg,
            weightChangeKgPerWeek: weightSlope ?? 0,
            waistChangeCmPerWeek: waistSlope,
            avgCalories: calSum / denom,
            calorieTarget: targets.calories,
            avgProtein: proSum / denom,
            proteinTarget: targets.protein,
            avgFiber: fibSum / denom,
            fiberTarget: targets.fiber,
            avgSteps: avgSteps,
            stepsTarget: targets.steps,
            trainingDaysPerWeek: profile.trainingDaysPerWeek,
            loggingDays: loggingDays,
            reportedLowEnergy: false,
            avgSleepHours: nil
        )
    }

    /// Least-squares slope (units per week) over recent dated points.
    static func weeklySlope(_ points: [(Date, Double)]) -> Double? {
        guard points.count >= 2 else { return nil }
        let sorted = points.sorted { $0.0 < $1.0 }
        guard let first = sorted.first?.0 else { return nil }
        // x in days since first point.
        let xs = sorted.map { $0.0.timeIntervalSince(first) / 86400.0 }
        let ys = sorted.map { $0.1 }
        let n = Double(xs.count)
        let sx = xs.reduce(0, +), sy = ys.reduce(0, +)
        let sxx = zip(xs, xs).map(*).reduce(0, +)
        let sxy = zip(xs, ys).map(*).reduce(0, +)
        let denom = n * sxx - sx * sx
        guard abs(denom) > 1e-9 else { return nil }
        let slopePerDay = (n * sxy - sx * sy) / denom
        return slopePerDay * 7.0
    }
}
