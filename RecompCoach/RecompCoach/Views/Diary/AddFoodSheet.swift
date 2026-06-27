import SwiftUI

/// Fast food logging: search + recents → pick → adjust portion → add.
/// Reused by the Diary, Dashboard quick action, and Diet Builder.
struct AddFoodSheet: View {
    @Environment(AppEnvironment.self) private var env
    @Environment(\.dismiss) private var dismiss

    var meal: MealType
    var onAdd: (FoodItem, Double, MealType) -> Void
    var onClose: () -> Void = {}

    @State private var query = ""
    @State private var results: [FoodItem] = []
    @State private var recents: [FoodItem] = []
    @State private var selectedMeal: MealType
    @State private var portionTarget: FoodItem?
    @State private var showCustom = false

    init(meal: MealType, onAdd: @escaping (FoodItem, Double, MealType) -> Void, onClose: @escaping () -> Void = {}) {
        self.meal = meal; self.onAdd = onAdd; self.onClose = onClose
        _selectedMeal = State(initialValue: meal)
    }

    var body: some View {
        NavigationStack {
            List {
                Section {
                    Picker("Meal", selection: $selectedMeal) {
                        ForEach(MealType.allCases) { Label($0.title, systemImage: $0.systemImage).tag($0) }
                    }.pickerStyle(.menu)
                }
                if query.isEmpty && !recents.isEmpty {
                    Section("Recent") { ForEach(recents) { row($0) } }
                }
                if !query.isEmpty {
                    Section("Results") {
                        if results.isEmpty {
                            Button { showCustom = true } label: {
                                Label("Add \"\(query)\" as a custom food", systemImage: "plus")
                            }
                        }
                        ForEach(results) { row($0) }
                    }
                }
            }
            .searchable(text: $query, prompt: "Search foods")
            .onChange(of: query) { _, _ in results = env.store.searchFoods(query, limit: 40) }
            .navigationTitle("Add Food")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) { Button("Close") { onClose(); dismiss() } }
                ToolbarItem(placement: .topBarTrailing) {
                    Button { showCustom = true } label: { Image(systemName: "square.and.pencil") }
                }
            }
            .task { recents = env.store.recentFoods(limit: 12) }
            .sheet(item: $portionTarget) { food in
                PortionSheet(food: food, meal: selectedMeal) { f, grams, m in
                    onAdd(f, grams, m); portionTarget = nil
                }
            }
            .sheet(isPresented: $showCustom) {
                CustomFoodSheet { food in
                    portionTarget = food
                }
            }
        }
    }

    private func row(_ food: FoodItem) -> some View {
        Button { portionTarget = food } label: {
            HStack {
                VStack(alignment: .leading) {
                    Text(food.name).foregroundStyle(.primary)
                    Text("\(Int(food.caloriesPerServing)) kcal · \(food.servingDescription)")
                        .font(.caption).foregroundStyle(.secondary)
                }
                Spacer()
                Image(systemName: "plus.circle.fill").foregroundStyle(Theme.accent)
            }
        }
    }
}

/// Adjust grams (or servings) before logging, with live macro preview.
struct PortionSheet: View {
    @Environment(\.dismiss) private var dismiss
    var food: FoodItem
    var meal: MealType
    var onConfirm: (FoodItem, Double, MealType) -> Void

    @State private var grams: Double
    init(food: FoodItem, meal: MealType, onConfirm: @escaping (FoodItem, Double, MealType) -> Void) {
        self.food = food; self.meal = meal; self.onConfirm = onConfirm
        _grams = State(initialValue: food.defaultServingGrams)
    }

    private var n: Nutrients { food.nutrients(forGrams: grams) }

    var body: some View {
        NavigationStack {
            Form {
                Section(food.name) {
                    HStack {
                        Text("Amount"); Spacer()
                        TextField("g", value: $grams, format: .number).keyboardType(.decimalPad)
                            .multilineTextAlignment(.trailing).frame(width: 90)
                        Text("g").foregroundStyle(.secondary)
                    }
                    HStack {
                        ForEach([food.defaultServingGrams, 50, 100, 150], id: \.self) { g in
                            Button("\(Int(g))g") { grams = g }.buttonStyle(.bordered).font(.caption)
                        }
                    }
                }
                Section("Nutrition") {
                    nutrientRow("Calories", n.calories, "kcal")
                    nutrientRow("Protein", n.protein, "g")
                    nutrientRow("Carbs", n.carbs, "g")
                    nutrientRow("Fat", n.fat, "g")
                    nutrientRow("Fiber", n.fiber, "g")
                }
            }
            .navigationTitle("Portion")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) { Button("Cancel") { dismiss() } }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Add") { onConfirm(food, grams, meal); dismiss() }.bold()
                }
            }
        }
        .presentationDetents([.medium, .large])
    }

    private func nutrientRow(_ t: String, _ v: Double, _ u: String) -> some View {
        HStack { Text(t); Spacer(); Text("\(v.clean) \(u)").foregroundStyle(.secondary).monospacedDigit() }
    }
}

/// Create a custom food (per-100g basis).
struct CustomFoodSheet: View {
    @Environment(AppEnvironment.self) private var env
    @Environment(\.dismiss) private var dismiss
    var onCreate: (FoodItem) -> Void

    @State private var name = ""
    @State private var serving = 100.0
    @State private var kcal = 0.0, protein = 0.0, carbs = 0.0, fat = 0.0, fiber = 0.0

    var body: some View {
        NavigationStack {
            Form {
                Section("Food") {
                    TextField("Name", text: $name)
                    LabeledNumber("Serving size", value: $serving, unit: "g")
                }
                Section("Per 100 g") {
                    LabeledNumber("Calories", value: $kcal, unit: "kcal")
                    LabeledNumber("Protein", value: $protein, unit: "g")
                    LabeledNumber("Carbs", value: $carbs, unit: "g")
                    LabeledNumber("Fat", value: $fat, unit: "g")
                    LabeledNumber("Fiber", value: $fiber, unit: "g")
                }
            }
            .navigationTitle("Custom Food")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) { Button("Cancel") { dismiss() } }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Save") {
                        let nutrients = Nutrients([.calories: kcal, .protein: protein, .carbs: carbs, .fat: fat, .fiber: fiber])
                        let food = env.store.upsertCustomFood(name: name, servingGrams: serving, per100g: nutrients)
                        onCreate(food); dismiss()
                    }.bold().disabled(name.isEmpty)
                }
            }
        }
    }
}
