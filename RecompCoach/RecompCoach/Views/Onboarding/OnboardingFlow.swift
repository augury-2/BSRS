import SwiftUI

struct OnboardingFlow: View {
    @Environment(AppEnvironment.self) private var env
    var onComplete: () -> Void
    @State private var vm: OnboardingViewModel?

    var body: some View {
        Group {
            if let vm { content(vm) } else { ProgressView().task { vm = OnboardingViewModel(store: env.store) } }
        }
    }

    @ViewBuilder
    private func content(_ vm: OnboardingViewModel) -> some View {
        @Bindable var vm = vm
        NavigationStack {
            VStack(spacing: 0) {
                ProgressView(value: Double(vm.step + 1), total: Double(vm.lastStep + 1))
                    .tint(Theme.accent).padding()

                TabView(selection: $vm.step) {
                    basics(vm).tag(0)
                    body(vm).tag(1)
                    goals(vm).tag(2)
                    summary(vm).tag(3)
                }
                .tabViewStyle(.page(indexDisplayMode: .never))
                .animation(.easeInOut, value: vm.step)

                footer(vm)
            }
            .navigationTitle("Set up your plan")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    // MARK: Steps

    private func basics(_ vm: OnboardingViewModel) -> some View {
        @Bindable var vm = vm
        return Form {
            Section("About you") {
                TextField("Name", text: $vm.name)
                Stepper("Age: \(vm.age)", value: $vm.age, in: 14...90)
                Picker("Sex", selection: $vm.sex) {
                    ForEach(Sex.allCases) { Text($0.title).tag($0) }
                }.pickerStyle(.segmented)
                Picker("Units", selection: $vm.units) {
                    Text("Metric (kg, cm)").tag(Units.metric)
                    Text("Imperial (lb, in)").tag(Units.imperial)
                }
            }
        }
    }

    private func body(_ vm: OnboardingViewModel) -> some View {
        @Bindable var vm = vm
        return Form {
            Section("Body") {
                LabeledNumber("Height", value: $vm.heightCm, unit: vm.units.lengthUnit)
                LabeledNumber("Current weight", value: $vm.weightKg, unit: vm.units.weightUnit)
            }
            Section("Optional metrics (improves accuracy)") {
                OptionalNumber("Body fat %", value: $vm.bodyFatPercent)
                OptionalNumber("Waist", value: $vm.waistCm)
                OptionalNumber("Hip", value: $vm.hipCm)
                OptionalNumber("Chest", value: $vm.chestCm)
                OptionalNumber("Thigh", value: $vm.thighCm)
                OptionalNumber("Arm", value: $vm.armCm)
            }
        }
    }

    private func goals(_ vm: OnboardingViewModel) -> some View {
        @Bindable var vm = vm
        return Form {
            Section("Goal") {
                Picker("Goal", selection: $vm.goal) {
                    ForEach(GoalType.allCases) { Text($0.title).tag($0) }
                }.pickerStyle(.inline).labelsHidden()
            }
            Section("Activity") {
                Picker("Activity level", selection: $vm.activity) {
                    ForEach(ActivityLevel.allCases) { Text($0.title).tag($0) }
                }
                Stepper("Training days/week: \(vm.trainingDays)", value: $vm.trainingDays, in: 0...7)
            }
        }
    }

    private func summary(_ vm: OnboardingViewModel) -> some View {
        let r = vm.previewResult
        return ScrollView {
            VStack(spacing: 14) {
                Card {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("Your daily plan").font(.headline)
                        Text("Maintenance ≈ \(Int(r.tdee)) kcal · BMR \(Int(r.bmr)) kcal")
                            .font(.caption).foregroundStyle(.secondary)
                    }
                }
                Card {
                    VStack(spacing: 12) {
                        MacroBar(title: "Calories", value: r.targets.calories, target: r.targets.calories, unit: "kcal", color: Theme.accent)
                        MacroBar(title: "Protein", value: r.targets.protein, target: r.targets.protein, unit: "g", color: Theme.protein)
                        MacroBar(title: "Carbs", value: r.targets.carbs, target: r.targets.carbs, unit: "g", color: Theme.carbs)
                        MacroBar(title: "Fat", value: r.targets.fat, target: r.targets.fat, unit: "g", color: Theme.fat)
                        MacroBar(title: "Fiber", value: r.targets.fiber, target: r.targets.fiber, unit: "g", color: Theme.fiber)
                    }
                }
                Card {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("Key micronutrients to watch").font(.subheadline.bold())
                        Text("Iron, calcium, magnesium, potassium, zinc, B12, vitamin D and vitamin C — tracked automatically as you log food.")
                            .font(.caption).foregroundStyle(.secondary)
                    }
                }
            }.padding()
        }
    }

    private func footer(_ vm: OnboardingViewModel) -> some View {
        HStack {
            if vm.step > 0 { Button("Back") { vm.back() }.buttonStyle(.bordered) }
            Spacer()
            if vm.step < vm.lastStep {
                Button("Continue") { vm.next() }
                    .buttonStyle(.borderedProminent)
                    .disabled(!vm.canAdvance)
            } else {
                Button("Get Started") { vm.finish(); onComplete() }
                    .buttonStyle(.borderedProminent)
            }
        }.padding()
    }
}

// MARK: - Small input helpers

struct LabeledNumber: View {
    let title: String
    @Binding var value: Double
    var unit: String
    init(_ t: String, value: Binding<Double>, unit: String) { title = t; _value = value; self.unit = unit }
    var body: some View {
        HStack {
            Text(title); Spacer()
            TextField("0", value: $value, format: .number).keyboardType(.decimalPad)
                .multilineTextAlignment(.trailing).frame(width: 90)
            Text(unit).foregroundStyle(.secondary)
        }
    }
}

struct OptionalNumber: View {
    let title: String
    @Binding var value: Double?
    init(_ t: String, value: Binding<Double?>) { title = t; _value = value }
    var body: some View {
        HStack {
            Text(title); Spacer()
            TextField("—", value: $value, format: .number).keyboardType(.decimalPad)
                .multilineTextAlignment(.trailing).frame(width: 90)
        }
    }
}

#Preview {
    OnboardingFlow(onComplete: {}).environment(AppEnvironment.preview())
}
