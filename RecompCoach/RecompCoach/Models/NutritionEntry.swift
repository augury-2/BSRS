import Foundation
import SwiftData

/// A single logged food in the diary. Stores a **snapshot** of the food's name
/// and computed nutrients so history stays correct even if the source food is
/// later edited or deleted.
@Model
final class NutritionEntry {
    @Attribute(.unique) var id: UUID
    var dayKey: String          // "yyyy-MM-dd" for fast per-day queries
    var loggedAt: Date
    var mealRaw: String
    var foodID: UUID?
    var foodName: String
    var quantityGrams: Double
    var nutrientsData: Data     // encoded snapshot of scaled Nutrients
    var updatedAt: Date

    init(id: UUID = UUID(),
         date: Date = .now,
         meal: MealType,
         foodID: UUID?,
         foodName: String,
         quantityGrams: Double,
         nutrients: Nutrients) {
        self.id = id
        self.dayKey = DayKey.string(from: date)
        self.loggedAt = date
        self.mealRaw = meal.rawValue
        self.foodID = foodID
        self.foodName = foodName
        self.quantityGrams = quantityGrams
        self.nutrientsData = (try? JSONEncoder().encode(nutrients)) ?? Data()
        self.updatedAt = .now
    }

    var meal: MealType { get { MealType(rawValue: mealRaw) ?? .snack } set { mealRaw = newValue.rawValue } }

    var nutrients: Nutrients {
        get { (try? JSONDecoder().decode(Nutrients.self, from: nutrientsData)) ?? .zero }
        set { nutrientsData = (try? JSONEncoder().encode(newValue)) ?? Data(); updatedAt = .now }
    }
}

enum DayKey {
    static let formatter: DateFormatter = {
        let f = DateFormatter()
        f.calendar = Calendar(identifier: .gregorian)
        f.locale = Locale(identifier: "en_US_POSIX")
        f.dateFormat = "yyyy-MM-dd"
        return f
    }()
    static func string(from date: Date) -> String { formatter.string(from: date) }
}
