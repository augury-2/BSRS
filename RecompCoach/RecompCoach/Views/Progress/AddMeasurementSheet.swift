import SwiftUI

/// Log weight + optional body composition / circumference measurements.
struct AddMeasurementSheet: View {
    @Environment(AppEnvironment.self) private var env
    @Environment(\.dismiss) private var dismiss
    var onSave: () -> Void = {}

    @State private var date = Date()
    @State private var weight: Double?
    @State private var bodyFat: Double?
    @State private var waist: Double?
    @State private var hip: Double?
    @State private var chest: Double?
    @State private var thigh: Double?
    @State private var arm: Double?

    var body: some View {
        NavigationStack {
            Form {
                Section { DatePicker("Date", selection: $date, displayedComponents: .date) }
                Section("Body") {
                    OptionalNumber("Weight", value: $weight)
                    OptionalNumber("Body fat %", value: $bodyFat)
                }
                Section("Measurements (cm)") {
                    OptionalNumber("Waist", value: $waist)
                    OptionalNumber("Hip", value: $hip)
                    OptionalNumber("Chest", value: $chest)
                    OptionalNumber("Thigh", value: $thigh)
                    OptionalNumber("Arm", value: $arm)
                }
            }
            .navigationTitle("Add Measurement")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) { Button("Cancel") { dismiss() } }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Save") {
                        let m = BodyMeasurement(date: date, weightKg: weight, bodyFatPercent: bodyFat,
                                                waistCm: waist, hipCm: hip, chestCm: chest,
                                                thighCm: thigh, armCm: arm)
                        env.store.addMeasurement(m)
                        if let w = weight, let p = env.store.currentProfile() {
                            p.currentWeightKg = w
                            p.targets = TargetsEngine.compute(for: p).targets
                            env.store.saveProfile(p)
                        }
                        onSave(); dismiss()
                    }.bold().disabled([weight, bodyFat, waist, hip, chest, thigh, arm].allSatisfy { $0 == nil })
                }
            }
        }
    }
}
