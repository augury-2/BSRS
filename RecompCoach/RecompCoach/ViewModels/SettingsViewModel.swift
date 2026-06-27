import Foundation
import Observation

@Observable
@MainActor
final class SettingsViewModel {
    private let env: AppEnvironment
    init(env: AppEnvironment) { self.env = env }

    var profile: UserProfile?
    var targets: NutritionTargets = .placeholder

    // Editable target fields
    var calorieText = ""
    var proteinText = ""
    var carbText = ""
    var fatText = ""
    var fiberText = ""
    var stepsText = ""

    func load() {
        guard let p = env.store.currentProfile() else { return }
        profile = p
        targets = p.targets ?? TargetsEngine.compute(for: p).targets
        calorieText = String(Int(targets.calories))
        proteinText = String(Int(targets.protein))
        carbText = String(Int(targets.carbs))
        fatText = String(Int(targets.fat))
        fiberText = String(Int(targets.fiber))
        stepsText = String(targets.steps)
    }

    func recalcFromProfile() {
        guard let p = profile else { return }
        let r = TargetsEngine.compute(for: p)
        p.targets = r.targets
        env.store.saveProfile(p)
        load()
    }

    func saveManualTargets() {
        guard let p = profile else { return }
        var t = targets
        t.calories = Double(calorieText) ?? t.calories
        t.protein  = Double(proteinText) ?? t.protein
        t.carbs    = Double(carbText) ?? t.carbs
        t.fat      = Double(fatText) ?? t.fat
        t.fiber    = Double(fiberText) ?? t.fiber
        t.steps    = Int(stepsText) ?? t.steps
        p.targets = t
        p.manualCalorieOverride = t.calories
        p.manualProteinOverride = t.protein
        env.store.saveProfile(p)
        load()
    }

    func setUnits(_ u: Units) { profile?.units = u; persist() }
    func setCloudSync(_ on: Bool) {
        profile?.cloudSyncEnabled = on
        env.sync.cloudSyncEnabled = on
        persist()
        if on { Task { await env.sync.sync() } }
    }
    func setHealthSync(_ on: Bool) async {
        profile?.healthSyncEnabled = on
        persist()
        if on { try? await env.activity.requestAuthorization() }
    }
    func setMealReminders(_ on: Bool) { profile?.mealReminders = on; persist() }
    func setWeighInReminders(_ on: Bool) { profile?.weighInReminders = on; persist() }

    private func persist() { if let p = profile { env.store.saveProfile(p) } }

    /// GDPR-style full data export, encrypted with the device key.
    func exportData() -> Data? {
        guard let p = profile else { return nil }
        let payload = ProfileDTO(p)
        guard let json = try? JSONEncoder.iso.encode(payload) else { return nil }
        return try? AppCrypto.seal(json)
    }
}
