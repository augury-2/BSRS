import Foundation
import Observation

@Observable
@MainActor
final class FoodDiaryViewModel {
    private let store: AppStore
    init(store: AppStore) { self.store = store }

    var date: Date = .now
    var entries: [NutritionEntry] = []
    var targets: NutritionTargets = .placeholder

    // Search sheet state
    var query = ""
    var results: [FoodItem] = []
    var recents: [FoodItem] = []

    func load() {
        if let p = store.currentProfile() {
            targets = p.targets ?? TargetsEngine.compute(for: p).targets
        }
        entries = store.entries(on: date)
        recents = store.recentFoods(limit: 12)
    }

    func entries(for meal: MealType) -> [NutritionEntry] { entries.filter { $0.meal == meal } }
    func total(for meal: MealType) -> Nutrients { NutritionCalculator.totals(entries(for: meal)) }
    var dayTotal: Nutrients { NutritionCalculator.totals(entries) }

    func search() {
        results = store.searchFoods(query, limit: 40)
    }

    func add(_ food: FoodItem, grams: Double, meal: MealType) {
        store.addEntry(food: food, grams: grams, meal: meal, date: date)
        load()
    }

    func delete(_ entry: NutritionEntry) {
        store.deleteEntry(entry)
        load()
    }

    func goToPreviousDay() { date = Calendar.current.date(byAdding: .day, value: -1, to: date)!; load() }
    func goToNextDay() { date = Calendar.current.date(byAdding: .day, value: 1, to: date)!; load() }

    var isToday: Bool { Calendar.current.isDateInToday(date) }
}
