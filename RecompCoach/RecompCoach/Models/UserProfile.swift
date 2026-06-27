import Foundation
import SwiftData

@Model
final class UserProfile {
    @Attribute(.unique) var id: UUID
    var name: String
    var age: Int
    var sexRaw: String
    var heightCm: Double
    var currentWeightKg: Double
    var goalRaw: String
    var activityRaw: String
    var trainingDaysPerWeek: Int
    var bodyFatPercent: Double?      // optional, improves protein/lean-mass estimates
    var unitsRaw: String

    // Preferences
    var cloudSyncEnabled: Bool
    var healthSyncEnabled: Bool
    var mealReminders: Bool
    var weighInReminders: Bool

    // Stored target snapshot + optional manual overrides
    var targetsData: Data?           // encoded NutritionTargets
    var manualCalorieOverride: Double?
    var manualProteinOverride: Double?

    var createdAt: Date
    var updatedAt: Date

    init(id: UUID = UUID(),
         name: String = "",
         age: Int = 30,
         sex: Sex = .male,
         heightCm: Double = 175,
         currentWeightKg: Double = 80,
         goal: GoalType = .loseFatMaintainMuscle,
         activity: ActivityLevel = .moderate,
         trainingDaysPerWeek: Int = 4,
         bodyFatPercent: Double? = nil,
         units: Units = .metric) {
        self.id = id
        self.name = name
        self.age = age
        self.sexRaw = sex.rawValue
        self.heightCm = heightCm
        self.currentWeightKg = currentWeightKg
        self.goalRaw = goal.rawValue
        self.activityRaw = activity.rawValue
        self.trainingDaysPerWeek = trainingDaysPerWeek
        self.bodyFatPercent = bodyFatPercent
        self.unitsRaw = units.rawValue
        self.cloudSyncEnabled = false
        self.healthSyncEnabled = false
        self.mealReminders = true
        self.weighInReminders = true
        self.targetsData = nil
        self.createdAt = .now
        self.updatedAt = .now
    }

    // Typed accessors
    var sex: Sex { get { Sex(rawValue: sexRaw) ?? .male } set { sexRaw = newValue.rawValue } }
    var goal: GoalType { get { GoalType(rawValue: goalRaw) ?? .loseFatMaintainMuscle } set { goalRaw = newValue.rawValue } }
    var activity: ActivityLevel { get { ActivityLevel(rawValue: activityRaw) ?? .moderate } set { activityRaw = newValue.rawValue } }
    var units: Units { get { Units(rawValue: unitsRaw) ?? .metric } set { unitsRaw = newValue.rawValue } }

    var targets: NutritionTargets? {
        get { targetsData.flatMap { try? JSONDecoder().decode(NutritionTargets.self, from: $0) } }
        set { targetsData = newValue.flatMap { try? JSONEncoder().encode($0) }; updatedAt = .now }
    }

    /// Estimated lean body mass (kg) when body-fat % is known.
    var leanMassKg: Double? {
        guard let bf = bodyFatPercent, bf > 0, bf < 60 else { return nil }
        return currentWeightKg * (1 - bf / 100)
    }
}
