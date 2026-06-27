import Foundation
import SwiftData

/// A food in the database. Nutrient values are stored **per 100 g** for a single
/// canonical basis; portions scale from there. `defaultServingGrams` powers
/// one-tap "1 serving" logging.
@Model
final class FoodItem {
    @Attribute(.unique) var id: UUID
    var name: String
    var brand: String?
    var barcode: String?
    var servingDescription: String      // e.g. "1 scoop (30 g)"
    var defaultServingGrams: Double
    var per100gData: Data               // encoded Nutrients
    var isCustom: Bool
    var sourceRaw: String
    var updatedAt: Date

    init(id: UUID = UUID(),
         name: String,
         brand: String? = nil,
         barcode: String? = nil,
         servingDescription: String,
         defaultServingGrams: Double,
         per100g: Nutrients,
         isCustom: Bool = false,
         source: DataSource = .seed) {
        self.id = id
        self.name = name
        self.brand = brand
        self.barcode = barcode
        self.servingDescription = servingDescription
        self.defaultServingGrams = defaultServingGrams
        self.per100gData = (try? JSONEncoder().encode(per100g)) ?? Data()
        self.isCustom = isCustom
        self.sourceRaw = source.rawValue
        self.updatedAt = .now
    }

    var per100g: Nutrients {
        get { (try? JSONDecoder().decode(Nutrients.self, from: per100gData)) ?? .zero }
        set { per100gData = (try? JSONEncoder().encode(newValue)) ?? Data(); updatedAt = .now }
    }

    /// Nutrients for an arbitrary gram amount.
    func nutrients(forGrams grams: Double) -> Nutrients {
        per100g.scaled(by: grams / 100.0)
    }

    var caloriesPerServing: Double {
        per100g[.calories] * defaultServingGrams / 100.0
    }
}
