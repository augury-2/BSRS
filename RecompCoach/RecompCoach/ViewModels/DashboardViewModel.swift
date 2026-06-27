import Foundation
import Observation

@Observable
@MainActor
final class DashboardViewModel {
    private let env: AppEnvironment
    init(env: AppEnvironment) { self.env = env }

    var profile: UserProfile?
    var targets: NutritionTargets = .placeholder
    var consumed: Nutrients = .zero
    var byMeal: [MealType: Nutrients] = [:]
    var activity: DailyActivity = .init(steps: 0, distanceMeters: 0, activeEnergyKcal: 0, activeMinutes: 0)
    var weightSeries: [(Date, Double)] = []
    var stepsSeries: [(Date, Int)] = []
    var topInsight: CoachingInsight?

    var bmr: Double = 0

    func load() async {
        guard let p = env.store.currentProfile() else { return }
        profile = p
        targets = p.targets ?? TargetsEngine.compute(for: p).targets
        bmr = TargetsEngine.basalMetabolicRate(for: p)

        let entries = env.store.entries(on: .now)
        consumed = NutritionCalculator.totals(entries)
        byMeal = NutritionCalculator.totalsByMeal(entries)

        await refreshActivity(for: p)
        loadWeekSeries()

        let snapshot = SnapshotBuilder.build(store: env.store, profile: p)
        topInsight = CoachingEngine.analyze(snapshot).first
    }

    private func refreshActivity(for p: UserProfile) async {
        if p.healthSyncEnabled {
            let a = await env.activity.todaysActivity()
            activity = a
            env.store.upsertSteps(a.steps, distanceMeters: a.distanceMeters,
                                  activeMinutes: a.activeMinutes, activeEnergy: a.activeEnergyKcal, on: .now)
        } else if let log = env.store.activity(on: .now).first(where: { $0.kind == .steps }) {
            activity = DailyActivity(steps: log.steps ?? 0,
                                     distanceMeters: log.distanceMeters ?? 0,
                                     activeEnergyKcal: log.energyKcal,
                                     activeMinutes: log.activeMinutes ?? 0)
        }
    }

    private func loadWeekSeries() {
        let cal = Calendar.current
        let from = cal.date(byAdding: .day, value: -6, to: cal.startOfDay(for: .now))!
        weightSeries = env.store.measurements()
            .compactMap { m in m.weightKg.map { (m.date, $0) } }
            .filter { $0.0 >= cal.date(byAdding: .day, value: -42, to: .now)! }
        let acts = env.store.activity(in: from...Date()).filter { $0.kind == .steps }
        stepsSeries = acts.compactMap { a in a.steps.map { (a.date, $0) } }
    }

    // Derived display values
    var workoutKcal: Double {
        env.store.activity(on: .now).filter { $0.kind != .steps }.reduce(0) { $0 + $1.energyKcal }
    }
    var caloriesOut: Double {
        NutritionCalculator.caloriesOut(
            bmr: bmr,
            activeEnergyKcal: activity.activeEnergyKcal > 0 ? activity.activeEnergyKcal : nil,
            steps: activity.steps, workoutKcal: workoutKcal,
            weightKg: profile?.currentWeightKg ?? 80)
    }
    var energyBalance: Double { NutritionCalculator.energyBalance(caloriesIn: consumed.calories, caloriesOut: caloriesOut) }

    func macroProgress(_ key: NutrientKey) -> Double {
        let target: Double
        switch key {
        case .calories: target = targets.calories
        case .protein:  target = targets.protein
        case .carbs:    target = targets.carbs
        case .fat:      target = targets.fat
        case .fiber:    target = targets.fiber
        default:        target = 1
        }
        guard target > 0 else { return 0 }
        return min(consumed[key] / target, 1.0)
    }
    var stepsProgress: Double {
        guard targets.steps > 0 else { return 0 }
        return min(Double(activity.steps) / Double(targets.steps), 1.0)
    }
}
