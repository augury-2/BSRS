import Foundation
import SwiftData

/// Seeds the bundled food database into SwiftData on first launch so search
/// works fully offline. When online, `/foods?since=` deltas merge on top.
struct FoodDatabaseSeeder {

    struct SeedFood: Codable {
        var name: String
        var brand: String?
        var servingDescription: String
        var defaultServingGrams: Double
        var per100g: Nutrients
    }

    @MainActor
    static func seedIfNeeded(context: ModelContext) {
        let countDescriptor = FetchDescriptor<FoodItem>()
        let existing = (try? context.fetchCount(countDescriptor)) ?? 0
        guard existing == 0 else { return }

        guard let url = Bundle.main.url(forResource: "foods", withExtension: "json"),
              let data = try? Data(contentsOf: url) else {
            assertionFailure("foods.json missing from bundle")
            return
        }
        do {
            let seeds = try JSONDecoder().decode([SeedFood].self, from: data)
            for s in seeds {
                let item = FoodItem(
                    name: s.name,
                    brand: s.brand,
                    servingDescription: s.servingDescription,
                    defaultServingGrams: s.defaultServingGrams,
                    per100g: s.per100g,
                    isCustom: false,
                    source: .seed
                )
                context.insert(item)
            }
            try context.save()
        } catch {
            assertionFailure("Failed to seed foods: \(error)")
        }
    }
}
