import SwiftUI

/// Manually log a workout with an estimated energy burn (METs-based).
struct AddWorkoutSheet: View {
    @Environment(AppEnvironment.self) private var env
    @Environment(\.dismiss) private var dismiss
    var onSave: () -> Void = {}

    struct Preset: Identifiable { let id = UUID(); let name: String; let met: Double; let kind: ActivityKind }
    private let presets: [Preset] = [
        .init(name: "Strength training", met: 5.0, kind: .strength),
        .init(name: "Walking (brisk)", met: 4.3, kind: .cardio),
        .init(name: "Incline treadmill", met: 6.0, kind: .cardio),
        .init(name: "Cycling (moderate)", met: 7.5, kind: .cardio),
        .init(name: "HIIT", met: 9.0, kind: .cardio),
        .init(name: "Yoga / mobility", met: 3.0, kind: .other)
    ]

    @State private var selected: Preset
    @State private var minutes: Double = 45

    init(onSave: @escaping () -> Void = {}) {
        self.onSave = onSave
        _selected = State(initialValue: Preset(name: "Strength training", met: 5.0, kind: .strength))
    }

    private var weight: Double { env.store.currentProfile()?.currentWeightKg ?? 80 }
    private var kcal: Double { NutritionCalculator.workoutEnergy(met: selected.met, minutes: minutes, weightKg: weight) }

    var body: some View {
        NavigationStack {
            Form {
                Section("Type") {
                    Picker("Workout", selection: Binding(get: { selected.name }, set: { name in
                        if let p = presets.first(where: { $0.name == name }) { selected = p }
                    })) {
                        ForEach(presets) { Text($0.name).tag($0.name) }
                    }
                }
                Section("Duration") {
                    Stepper("\(Int(minutes)) min", value: $minutes, in: 5...240, step: 5)
                }
                Section("Estimated energy") {
                    Text("≈ \(Int(kcal)) kcal")
                        .font(.title3.bold()).foregroundStyle(Theme.protein)
                    Text("Estimate uses METs × bodyweight × time. Edit later if needed.")
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Log Workout")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) { Button("Cancel") { dismiss() } }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Save") {
                        env.store.addWorkout(ActivityLog(date: .now, kind: selected.kind,
                                                         name: selected.name, source: .manual,
                                                         durationMinutes: minutes, energyKcal: kcal))
                        onSave(); dismiss()
                    }.bold()
                }
            }
        }
    }
}
