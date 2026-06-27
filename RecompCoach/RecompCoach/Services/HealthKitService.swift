import Foundation
#if canImport(HealthKit)
import HealthKit
#endif

struct DailyActivity: Equatable {
    var steps: Int
    var distanceMeters: Double
    var activeEnergyKcal: Double
    var activeMinutes: Int
}

/// Reads steps, walking distance, active energy and exercise minutes from
/// HealthKit. All methods degrade gracefully (return zeros / throw) when
/// HealthKit is unavailable or permission is denied, so the app stays usable.
protocol ActivityProviding {
    func requestAuthorization() async throws
    func todaysActivity() async -> DailyActivity
    func activity(for date: Date) async -> DailyActivity
}

#if canImport(HealthKit)
final class HealthKitService: ActivityProviding {
    private let store = HKHealthStore()

    private var readTypes: Set<HKObjectType> {
        var set = Set<HKObjectType>()
        if let steps = HKQuantityType.quantityType(forIdentifier: .stepCount) { set.insert(steps) }
        if let dist = HKQuantityType.quantityType(forIdentifier: .distanceWalkingRunning) { set.insert(dist) }
        if let energy = HKQuantityType.quantityType(forIdentifier: .activeEnergyBurned) { set.insert(energy) }
        if let exercise = HKQuantityType.quantityType(forIdentifier: .appleExerciseTime) { set.insert(exercise) }
        return set
    }

    func requestAuthorization() async throws {
        guard HKHealthStore.isHealthDataAvailable() else { return }
        try await store.requestAuthorization(toShare: [], read: readTypes)
    }

    func todaysActivity() async -> DailyActivity { await activity(for: .now) }

    func activity(for date: Date) async -> DailyActivity {
        guard HKHealthStore.isHealthDataAvailable() else {
            return DailyActivity(steps: 0, distanceMeters: 0, activeEnergyKcal: 0, activeMinutes: 0)
        }
        let cal = Calendar.current
        let start = cal.startOfDay(for: date)
        let end = cal.date(byAdding: .day, value: 1, to: start) ?? date
        let predicate = HKQuery.predicateForSamples(withStart: start, end: end)

        async let steps = sum(.stepCount, unit: .count(), predicate: predicate)
        async let dist = sum(.distanceWalkingRunning, unit: .meter(), predicate: predicate)
        async let energy = sum(.activeEnergyBurned, unit: .kilocalorie(), predicate: predicate)
        async let exercise = sum(.appleExerciseTime, unit: .minute(), predicate: predicate)

        return DailyActivity(
            steps: Int(await steps),
            distanceMeters: await dist,
            activeEnergyKcal: await energy,
            activeMinutes: Int(await exercise)
        )
    }

    private func sum(_ id: HKQuantityTypeIdentifier, unit: HKUnit, predicate: NSPredicate) async -> Double {
        guard let type = HKQuantityType.quantityType(forIdentifier: id) else { return 0 }
        return await withCheckedContinuation { cont in
            let q = HKStatisticsQuery(quantityType: type, quantitySamplePredicate: predicate, options: .cumulativeSum) { _, stats, _ in
                cont.resume(returning: stats?.sumQuantity()?.doubleValue(for: unit) ?? 0)
            }
            store.execute(q)
        }
    }
}
#endif

/// Fallback used in Previews, simulator without Health, or unit tests.
final class MockActivityProvider: ActivityProviding {
    func requestAuthorization() async throws {}
    func todaysActivity() async -> DailyActivity {
        DailyActivity(steps: 7421, distanceMeters: 5320, activeEnergyKcal: 410, activeMinutes: 38)
    }
    func activity(for date: Date) async -> DailyActivity { await todaysActivity() }
}
