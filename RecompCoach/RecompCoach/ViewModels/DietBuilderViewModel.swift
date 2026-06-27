import Foundation
import Observation

/// Powers the "Build My Diet" screen: add foods + portions, recalc everything
/// live, view macro split + micronutrient radar, save/reuse as a template.
@Observable
@MainActor
final class DietBuilderViewModel {
    struct Line: Identifiable, Equatable {
        let id = UUID()
        var food: FoodItem
        var grams: Double
        var nutrients: Nutrients { food.nutrients(forGrams: grams) }
    }

    private let store: AppStore
    init(store: AppStore) { self.store = store }

    var lines: [Line] = []
    var targets: NutritionTargets = .placeholder

    // search
    var query = ""
    var results: [FoodItem] = []

    func load() {
        if let p = store.currentProfile() {
            targets = p.targets ?? TargetsEngine.compute(for: p).targets
        }
    }

    func search() { results = store.searchFoods(query, limit: 40) }

    func add(_ food: FoodItem) {
        lines.append(Line(food: food, grams: food.defaultServingGrams))
    }
    func remove(at offsets: IndexSet) { lines.remove(atOffsets: offsets) }
    func updateGrams(_ line: Line, grams: Double) {
        guard let idx = lines.firstIndex(of: line) else { return }
        lines[idx].grams = max(0, grams)
    }

    // Live recomputation
    var total: Nutrients { NutritionCalculator.totals(asEntries()) }

    private func asEntries() -> [NutritionEntry] {
        lines.map { NutritionEntry(meal: .snack, foodID: $0.food.id, foodName: $0.food.name,
                                   quantityGrams: $0.grams, nutrients: $0.nutrients) }
    }

    /// Macro energy split (% of calories) for the pie/bar.
    var macroSplit: [(NutrientKey, Double)] {
        let p = total.protein * 4, c = total.carbs * 4, f = total.fat * 9
        let sum = max(p + c + f, 1)
        return [(.protein, p / sum), (.carbs, c / sum), (.fat, f / sum)]
    }

    /// % of RDA per radar nutrient (capped at 150 for display).
    var radar: [(NutrientKey, Double)] {
        let pct = NutritionCalculator.percentRDA(total, targets: targets)
        return NutrientKey.radarKeys.map { ($0, min(pct[$0] ?? 0, 150)) }
    }

    var highlights: (high: [NutrientKey], low: [NutrientKey]) {
        NutritionCalculator.highlights(total, targets: targets)
    }

    func saveAsTemplate(name: String, kind: TemplateKind) {
        let items = lines.map { TemplateItem(foodID: $0.food.id, foodName: $0.food.name, grams: $0.grams) }
        store.saveTemplate(MealTemplate(name: name, kind: kind, items: items))
    }

    func loadTemplate(_ t: MealTemplate) {
        lines = t.items.compactMap { item in
            store.food(by: item.foodID).map { Line(food: $0, grams: item.grams) }
        }
    }

    /// Log the whole built diet to today's diary under the given meal.
    func logToDiary(meal: MealType, date: Date = .now) {
        for line in lines {
            store.addEntry(food: line.food, grams: line.grams, meal: meal, date: date)
        }
    }

    func templates() -> [MealTemplate] { store.templates() }
}
