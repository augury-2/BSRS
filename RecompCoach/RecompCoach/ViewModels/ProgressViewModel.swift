import Foundation
import Observation

@Observable
@MainActor
final class ProgressViewModel {
    private let store: AppStore
    init(store: AppStore) { self.store = store }

    var measurements: [BodyMeasurement] = []
    var snapshot: WeeklySnapshot?
    var insights: [CoachingInsight] = []
    var trendSummary: String = ""

    func load() {
        measurements = store.measurements().sorted { $0.date < $1.date }
        guard let p = store.currentProfile() else { return }
        let snap = SnapshotBuilder.build(store: store, profile: p)
        snapshot = snap
        insights = CoachingEngine.analyze(snap)
        trendSummary = CoachingEngine.classifyTrend(
            weightChangeKgPerWeek: snap.weightChangeKgPerWeek,
            waistChangeCmPerWeek: snap.waistChangeCmPerWeek,
            bodyWeightKg: snap.bodyWeightKg)
    }

    func addMeasurement(weight: Double?, bodyFat: Double?, waist: Double?, hip: Double?,
                        chest: Double?, thigh: Double?, arm: Double?, date: Date) {
        store.addMeasurement(BodyMeasurement(date: date, weightKg: weight, bodyFatPercent: bodyFat,
                                             waistCm: waist, hipCm: hip, chestCm: chest,
                                             thighCm: thigh, armCm: arm))
        // Keep the profile's current weight in sync with the latest entry.
        if let w = weight, let p = store.currentProfile() {
            p.currentWeightKg = w
            p.targets = TargetsEngine.compute(for: p).targets
            store.saveProfile(p)
        }
        load()
    }

    func delete(_ m: BodyMeasurement) { store.deleteMeasurement(m); load() }

    // Series for charts
    func series(_ keyPath: KeyPath<BodyMeasurement, Double?>) -> [(Date, Double)] {
        measurements.compactMap { m in m[keyPath: keyPath].map { (m.date, $0) } }
    }
}
