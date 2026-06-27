import Foundation
import Observation

@Observable
@MainActor
final class OnboardingViewModel {
    // Collected fields
    var name = ""
    var age = 28
    var sex: Sex = .male
    var heightCm = 174.0
    var weightKg = 80.0
    var goal: GoalType = .loseFatMaintainMuscle
    var activity: ActivityLevel = .moderate
    var trainingDays = 4
    var units: Units = .metric

    // Optional metrics
    var bodyFatPercent: Double? = nil
    var waistCm: Double? = nil
    var hipCm: Double? = nil
    var chestCm: Double? = nil
    var thighCm: Double? = nil
    var armCm: Double? = nil

    var step = 0
    let lastStep = 3

    private let store: AppStore
    init(store: AppStore) { self.store = store }

    /// Live target preview shown on the summary step.
    var previewProfile: UserProfile {
        let p = UserProfile(name: name, age: age, sex: sex, heightCm: heightCm,
                            currentWeightKg: weightKg, goal: goal, activity: activity,
                            trainingDaysPerWeek: trainingDays, bodyFatPercent: bodyFatPercent,
                            units: units)
        return p
    }

    var previewResult: TargetsEngine.Result { TargetsEngine.compute(for: previewProfile) }

    var canAdvance: Bool {
        switch step {
        case 0: return !name.trimmingCharacters(in: .whitespaces).isEmpty && age > 0
        case 1: return heightCm > 0 && weightKg > 0
        default: return true
        }
    }

    func next() { if step < lastStep { step += 1 } }
    func back() { if step > 0 { step -= 1 } }

    func finish() {
        let profile = previewProfile
        profile.targets = TargetsEngine.compute(for: profile).targets
        store.saveProfile(profile)

        // Persist any optional baseline measurements.
        if [bodyFatPercent, waistCm, hipCm, chestCm, thighCm, armCm].contains(where: { $0 != nil }) {
            store.addMeasurement(BodyMeasurement(
                date: .now, weightKg: weightKg, bodyFatPercent: bodyFatPercent,
                waistCm: waistCm, hipCm: hipCm, chestCm: chestCm, thighCm: thighCm, armCm: armCm))
        } else {
            store.addMeasurement(BodyMeasurement(date: .now, weightKg: weightKg))
        }
    }
}
