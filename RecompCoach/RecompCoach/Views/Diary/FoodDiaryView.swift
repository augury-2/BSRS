import SwiftUI

struct FoodDiaryView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var vm: FoodDiaryViewModel?
    @State private var addMeal: MealType?

    var body: some View {
        NavigationStack {
            Group {
                if let vm { content(vm) }
                else { ProgressView().task { let v = FoodDiaryViewModel(store: env.store); v.load(); vm = v } }
            }
            .navigationTitle("Diary")
        }
    }

    @ViewBuilder
    private func content(_ vm: FoodDiaryViewModel) -> some View {
        List {
            Section { dayHeader(vm); totalsRow(vm) }
            ForEach(MealType.allCases) { meal in
                Section {
                    ForEach(vm.entries(for: meal)) { entry in
                        HStack {
                            VStack(alignment: .leading) {
                                Text(entry.foodName)
                                Text("\(Int(entry.quantityGrams)) g").font(.caption).foregroundStyle(.secondary)
                            }
                            Spacer()
                            Text("\(Int(entry.nutrients.calories)) kcal").foregroundStyle(.secondary).monospacedDigit()
                        }
                        .swipeActions { Button("Delete", role: .destructive) { vm.delete(entry) } }
                    }
                    Button { addMeal = meal } label: { Label("Add food", systemImage: "plus") }
                        .font(.subheadline)
                } header: {
                    HStack {
                        Label(meal.title, systemImage: meal.systemImage)
                        Spacer()
                        Text("\(Int(vm.total(for: meal).calories)) kcal").foregroundStyle(.secondary)
                    }
                }
            }
        }
        .sheet(item: $addMeal) { meal in
            AddFoodSheet(meal: meal) { food, grams, m in
                vm.add(food, grams: grams, meal: m)
            } onClose: { vm.load() }
        }
    }

    private func dayHeader(_ vm: FoodDiaryViewModel) -> some View {
        HStack {
            Button { vm.goToPreviousDay() } label: { Image(systemName: "chevron.left") }
            Spacer()
            Text(vm.isToday ? "Today" : vm.date.formatted(date: .abbreviated, time: .omitted)).font(.headline)
            Spacer()
            Button { vm.goToNextDay() } label: { Image(systemName: "chevron.right") }
                .disabled(vm.isToday)
        }
    }

    private func totalsRow(_ vm: FoodDiaryViewModel) -> some View {
        let t = vm.dayTotal
        return VStack(spacing: 10) {
            MacroBar(title: "Calories", value: t.calories, target: vm.targets.calories, unit: "kcal", color: Theme.accent)
            HStack(spacing: 14) {
                miniMacro("P", t.protein, vm.targets.protein, Theme.protein)
                miniMacro("C", t.carbs, vm.targets.carbs, Theme.carbs)
                miniMacro("F", t.fat, vm.targets.fat, Theme.fat)
                miniMacro("Fiber", t.fiber, vm.targets.fiber, Theme.fiber)
            }
        }
    }

    private func miniMacro(_ label: String, _ v: Double, _ target: Double, _ color: Color) -> some View {
        VStack(spacing: 2) {
            Text("\(Int(v))").font(.subheadline.bold()).foregroundStyle(color)
            Text("\(label) /\(Int(target))").font(.caption2).foregroundStyle(.secondary)
        }.frame(maxWidth: .infinity)
    }
}

#Preview { FoodDiaryView().environment(AppEnvironment.preview()) }
