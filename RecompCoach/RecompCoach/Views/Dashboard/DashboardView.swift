import SwiftUI

struct DashboardView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var vm: DashboardViewModel?
    @State private var sheet: Sheet?

    enum Sheet: Identifiable { case logFood, logWorkout, addMeasurement
        var id: Int { hashValue } }

    var body: some View {
        NavigationStack {
            Group {
                if let vm { content(vm) }
                else { ProgressView().task { vm = DashboardViewModel(env: env); await vm?.load() } }
            }
            .navigationTitle("Today")
            .toolbar { ToolbarItem(placement: .topBarTrailing) { ConnectivityPill(isOnline: env.reachability.isOnline) } }
            .sheet(item: $sheet) { which in
                switch which {
                case .logFood:
                    AddFoodSheet(meal: .snack) { food, grams, meal in
                        env.store.addEntry(food: food, grams: grams, meal: meal, date: .now)
                    } onClose: { Task { await vm?.load() } }
                case .logWorkout:
                    AddWorkoutSheet { Task { await vm?.load() } }
                case .addMeasurement:
                    AddMeasurementSheet { Task { await vm?.load() } }
                }
            }
        }
    }

    @ViewBuilder
    private func content(_ vm: DashboardViewModel) -> some View {
        ScrollView {
            VStack(spacing: 16) {
                ringsRow(vm)
                energyCard(vm)
                macrosCard(vm)
                quickActions
                if let insight = vm.topInsight {
                    NavigationLink { CoachView() } label: { InsightCard(insight: insight) }
                        .buttonStyle(.plain)
                }
                weekCard(vm)
                NavigationLink { ActivityView() } label: { stepsCard(vm) }
                    .buttonStyle(.plain)
            }
            .padding()
        }
        .refreshable { await vm.load() }
    }

    private func ringsRow(_ vm: DashboardViewModel) -> some View {
        Card {
            HStack {
                ProgressRing(progress: vm.macroProgress(.calories), color: Theme.accent,
                             title: "Calories",
                             value: Int(vm.consumed.calories).formatted(),
                             subtitle: "of \(Int(vm.targets.calories))")
                Spacer()
                ProgressRing(progress: vm.stepsProgress, color: Theme.steps,
                             title: "Steps",
                             value: vm.activity.steps.formatted(),
                             subtitle: "of \(vm.targets.steps.formatted())")
            }
        }
    }

    private func energyCard(_ vm: DashboardViewModel) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 10) {
                Text("Energy balance").font(.headline)
                HStack {
                    StatTile(systemImage: "fork.knife", title: "In", value: "\(Int(vm.consumed.calories)) kcal", tint: Theme.carbs)
                    StatTile(systemImage: "flame.fill", title: "Out (est.)", value: "\(Int(vm.caloriesOut)) kcal", tint: Theme.protein)
                }
                let bal = vm.energyBalance
                Text(bal <= 0 ? "≈ \(Int(-bal)) kcal deficit" : "≈ \(Int(bal)) kcal surplus")
                    .font(.subheadline.bold())
                    .foregroundStyle(bal <= 0 ? Theme.fiber : Theme.carbs)
            }
        }
    }

    private func macrosCard(_ vm: DashboardViewModel) -> some View {
        Card {
            VStack(spacing: 12) {
                MacroBar(title: "Protein", value: vm.consumed.protein, target: vm.targets.protein, unit: "g", color: Theme.protein)
                MacroBar(title: "Carbs", value: vm.consumed.carbs, target: vm.targets.carbs, unit: "g", color: Theme.carbs)
                MacroBar(title: "Fat", value: vm.consumed.fat, target: vm.targets.fat, unit: "g", color: Theme.fat)
                MacroBar(title: "Fiber", value: vm.consumed.fiber, target: vm.targets.fiber, unit: "g", color: Theme.fiber)
            }
        }
    }

    private var quickActions: some View {
        HStack(spacing: 10) {
            QuickAction(title: "Log Food", icon: "plus.circle.fill", tint: Theme.accent) { sheet = .logFood }
            QuickAction(title: "Workout", icon: "figure.strengthtraining.traditional", tint: Theme.protein) { sheet = .logWorkout }
            QuickAction(title: "Measure", icon: "ruler.fill", tint: Theme.fat) { sheet = .addMeasurement }
            QuickAction(title: "Weight", icon: "scalemass.fill", tint: Theme.steps) { sheet = .addMeasurement }
        }
    }

    private func weekCard(_ vm: DashboardViewModel) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 8) {
                Text("This week").font(.headline)
                Text("Weight").font(.caption).foregroundStyle(.secondary)
                TrendChart(vm.weightSeries, color: Theme.accent, unit: "kg")
                Text("Steps").font(.caption).foregroundStyle(.secondary)
                StepsBarChart(points: vm.stepsSeries, target: vm.targets.steps)
            }
        }
    }

    private func stepsCard(_ vm: DashboardViewModel) -> some View {
        Card {
            HStack {
                StatTile(systemImage: "figure.walk", title: "Distance",
                         value: String(format: "%.2f km", vm.activity.distanceMeters / 1000), tint: Theme.steps)
                StatTile(systemImage: "timer", title: "Active min",
                         value: "\(vm.activity.activeMinutes)", tint: Theme.fiber)
                Image(systemName: "chevron.right").foregroundStyle(.tertiary)
            }
        }
    }
}

struct QuickAction: View {
    var title: String; var icon: String; var tint: Color; var action: () -> Void
    var body: some View {
        Button(action: action) {
            VStack(spacing: 6) {
                Image(systemName: icon).font(.title3)
                Text(title).font(.caption2.weight(.semibold))
            }
            .frame(maxWidth: .infinity).padding(.vertical, 12)
            .background(tint.opacity(0.15), in: RoundedRectangle(cornerRadius: 14))
            .foregroundStyle(tint)
        }
    }
}

#Preview { DashboardView().environment(AppEnvironment.preview()) }
