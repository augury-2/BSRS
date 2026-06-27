import Foundation

/// Codable transfer objects for the REST sync contract (see Backend/API.md).
/// Kept separate from @Model classes so the wire format is stable.

struct ProfileDTO: Codable {
    var id: UUID
    var name: String
    var age: Int
    var sex: String
    var heightCm: Double
    var currentWeightKg: Double
    var goal: String
    var activity: String
    var trainingDaysPerWeek: Int
    var bodyFatPercent: Double?
    var units: String
    var updatedAt: Date

    init(_ p: UserProfile) {
        id = p.id; name = p.name; age = p.age; sex = p.sexRaw
        heightCm = p.heightCm; currentWeightKg = p.currentWeightKg
        goal = p.goalRaw; activity = p.activityRaw
        trainingDaysPerWeek = p.trainingDaysPerWeek
        bodyFatPercent = p.bodyFatPercent; units = p.unitsRaw
        updatedAt = p.updatedAt
    }
}

struct FoodDTO: Codable {
    var id: UUID
    var name: String
    var brand: String?
    var servingDescription: String
    var defaultServingGrams: Double
    var per100g: Nutrients
    var isCustom: Bool
    var updatedAt: Date

    init(_ f: FoodItem) {
        id = f.id; name = f.name; brand = f.brand
        servingDescription = f.servingDescription
        defaultServingGrams = f.defaultServingGrams
        per100g = f.per100g; isCustom = f.isCustom; updatedAt = f.updatedAt
    }
}

struct EntryDTO: Codable {
    var id: UUID
    var dayKey: String
    var loggedAt: Date
    var meal: String
    var foodID: UUID?
    var foodName: String
    var quantityGrams: Double
    var nutrients: Nutrients
    var updatedAt: Date

    init(_ e: NutritionEntry) {
        id = e.id; dayKey = e.dayKey; loggedAt = e.loggedAt; meal = e.mealRaw
        foodID = e.foodID; foodName = e.foodName; quantityGrams = e.quantityGrams
        nutrients = e.nutrients; updatedAt = e.updatedAt
    }
}

struct MeasurementDTO: Codable {
    var id: UUID
    var date: Date
    var weightKg: Double?
    var bodyFatPercent: Double?
    var waistCm: Double?
    var hipCm: Double?
    var chestCm: Double?
    var thighCm: Double?
    var armCm: Double?
    var updatedAt: Date

    init(_ m: BodyMeasurement) {
        id = m.id; date = m.date; weightKg = m.weightKg; bodyFatPercent = m.bodyFatPercent
        waistCm = m.waistCm; hipCm = m.hipCm; chestCm = m.chestCm
        thighCm = m.thighCm; armCm = m.armCm; updatedAt = m.updatedAt
    }
}

/// Outbox op as sent to /sync/push.
struct SyncOp: Codable {
    var id: UUID
    var entity: String
    var type: String
    var updatedAt: Date
    var payload: Data?
}
