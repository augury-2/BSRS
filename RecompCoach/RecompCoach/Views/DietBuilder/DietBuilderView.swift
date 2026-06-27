import SwiftUI

/// "Build My Diet": add foods + portions, recalc macros & micros live, view the
/// macro split + micronutrient radar, then save as a reusable template or log it.
struct DietBuilderView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var vm: DietBuilderViewModel?
    @State private var showAdd = false
    @State private var showSave = false
    @State private var showTemplates = false

    var body: some View {
        NavigationStack {
            Group {
                if let vm { content(vm) }
                else { ProgressView().task { let v = DietBuilderViewModel(store: env.store); v.load(); vm = v } }
            }
            .navigationTitle("Build My Diet")
        }
    }

    @ViewBuilder
    private func content(_ vm: DietBuilderViewModel) -> some View {
        ScrollView {
            VStack(spacing: 16) {
                summaryCard(vm)
                macroSplitCard(vm)
                radarCard(vm)
                itemsCard(vm)
            }.padding()
        }
        .toolbar {
            ToolbarItem(placement: .topBarLeading) {
                Button { showTemplates = true } label: { Image(systemName: "tray.full") }
            }
            ToolbarItem(placement: .topBarTrailing) {
                Menu {
                    Button { showAdd = true } label: { Label("Add food", systemImage: "plus") }
                    Button { showSave = true } label: { Label("Save as template", systemImage: "square.and.arrow.down") }
                        .disabled(vm.lines.isEmpty)
                    Menu("Log to diary") {
                        ForEach(MealType.allCases) { meal in
                            Button(meal.title) { vm.logToDiary(meal: meal) }
                        }
                    }.disabled(vm.lines.isEmpty)
                } label: { Image(systemName: "ellipsis.circle") }
            }
        }
        .sheet(isPresented: $showAdd) {
            AddFoodSheet(meal: .snack) { food, grams, _ in
                vm.lines.append(DietBuilderViewModel.Line(food: food, grams: grams))
            }
        }
        .sheet(isPresented: $showSave) { SaveTemplateSheet { name, kind in vm.saveAsTemplate(name: name, kind: kind) } }
        .sheet(isPresented: $showTemplates) {
            TemplatePickerSheet(templates: vm.templates()) { t in vm.loadTemplate(t); showTemplates = false }
        }
    }

    private func summaryCard(_ vm: DietBuilderViewModel) -> some View {
        let t = vm.total
        return Card {
            VStack(spacing: 12) {
                HStack {
                    Text("Day total").font(.headline)
                    Spacer()
                    Text("\(Int(t.calories)) kcal").font(.headline).foregroundStyle(Theme.accent)
                }
                MacroBar(title: "Protein", value: t.protein, target: vm.targets.protein, unit: "g", color: Theme.protein)
                MacroBar(title: "Carbs", value: t.carbs, target: vm.targets.carbs, unit: "g", color: Theme.carbs)
                MacroBar(title: "Fat", value: t.fat, target: vm.targets.fat, unit: "g", color: Theme.fat)
                MacroBar(title: "Fiber", value: t.fiber, target: vm.targets.fiber, unit: "g", color: Theme.fiber)
            }
        }
    }

    private func macroSplitCard(_ vm: DietBuilderViewModel) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 10) {
                Text("Macro split (% of calories)").font(.subheadline.bold())
                GeometryReader { geo in
                    HStack(spacing: 2) {
                        ForEach(vm.macroSplit, id: \.0) { (key, frac) in
                            Theme.color(for: key)
                                .frame(width: max(2, geo.size.width * frac))
                        }
                    }.clipShape(Capsule())
                }.frame(height: 14)
                HStack(spacing: 16) {
                    ForEach(vm.macroSplit, id: \.0) { (key, frac) in
                        HStack(spacing: 5) {
                            Circle().fill(Theme.color(for: key)).frame(width: 9, height: 9)
                            Text("\(key.displayName) \(Int(frac * 100))%").font(.caption)
                        }
                    }
                }
            }
        }
    }

    private func radarCard(_ vm: DietBuilderViewModel) -> some View {
        let hl = vm.highlights
        return Card {
            VStack(alignment: .leading, spacing: 8) {
                Text("Micronutrients (% of RDA)").font(.subheadline.bold())
                RadarChartView(data: vm.radar)
                if !hl.high.isEmpty {
                    Text("High in: " + hl.high.map(\.displayName).joined(separator: ", "))
                        .font(.caption).foregroundStyle(Theme.fiber)
                }
                if !hl.low.isEmpty {
                    Text("Low in: " + hl.low.map(\.displayName).joined(separator: ", "))
                        .font(.caption).foregroundStyle(Theme.protein)
                }
            }
        }
    }

    private func itemsCard(_ vm: DietBuilderViewModel) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 10) {
                Text("Foods").font(.subheadline.bold())
                if vm.lines.isEmpty {
                    Text("Add foods to build a day or meal. Adjust grams to see totals update instantly.")
                        .font(.caption).foregroundStyle(.secondary)
                }
                ForEach(vm.lines) { line in
                    HStack {
                        Text(line.food.name).lineLimit(1)
                        Spacer()
                        Stepper(value: Binding(
                            get: { line.grams },
                            set: { vm.updateGrams(line, grams: $0) }), in: 0...1000, step: 10) {
                            Text("\(Int(line.grams)) g").monospacedDigit().font(.caption)
                        }.labelsHidden().fixedSize()
                        Text("\(Int(line.nutrients.calories)) kcal")
                            .font(.caption).foregroundStyle(.secondary).frame(width: 64, alignment: .trailing)
                    }
                }
                .onDelete { vm.remove(at: $0) }
            }
        }
    }
}

struct SaveTemplateSheet: View {
    @Environment(\.dismiss) private var dismiss
    var onSave: (String, TemplateKind) -> Void
    @State private var name = ""
    @State private var kind: TemplateKind = .trainingDay
    var body: some View {
        NavigationStack {
            Form {
                TextField("Template name", text: $name)
                Picker("Type", selection: $kind) { ForEach(TemplateKind.allCases) { Text($0.title).tag($0) } }
            }
            .navigationTitle("Save Template").navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) { Button("Cancel") { dismiss() } }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Save") { onSave(name.isEmpty ? kind.title : name, kind); dismiss() }.bold()
                }
            }
        }.presentationDetents([.height(220)])
    }
}

struct TemplatePickerSheet: View {
    @Environment(\.dismiss) private var dismiss
    var templates: [MealTemplate]
    var onPick: (MealTemplate) -> Void
    var body: some View {
        NavigationStack {
            List {
                if templates.isEmpty { ContentUnavailableView("No templates", systemImage: "tray", description: Text("Save a built diet to reuse it later.")) }
                ForEach(templates) { t in
                    Button { onPick(t) } label: {
                        VStack(alignment: .leading) {
                            Text(t.name)
                            Text("\(t.kind.title) · \(t.items.count) items").font(.caption).foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Templates").navigationBarTitleDisplayMode(.inline)
            .toolbar { ToolbarItem(placement: .topBarTrailing) { Button("Close") { dismiss() } } }
        }
    }
}

#Preview { DietBuilderView().environment(AppEnvironment.preview()) }
