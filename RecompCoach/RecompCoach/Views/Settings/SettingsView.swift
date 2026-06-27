import SwiftUI

struct SettingsView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var vm: SettingsViewModel?
    @State private var showDeleteConfirm = false
    @State private var exportURL: URL?

    var body: some View {
        NavigationStack {
            Group {
                if let vm { content(vm) }
                else { ProgressView().task { let v = SettingsViewModel(env: env); v.load(); vm = v } }
            }
            .navigationTitle("Settings")
        }
    }

    @ViewBuilder
    private func content(_ vm: SettingsViewModel) -> some View {
        @Bindable var vm = vm
        Form {
            if let p = vm.profile {
                Section("Profile") {
                    LabeledContent("Name", value: p.name)
                    LabeledContent("Goal", value: p.goal.title)
                    LabeledContent("Weight", value: "\(p.currentWeightKg.clean) \(p.units.weightUnit)")
                }
            }

            Section("Daily targets") {
                targetField("Calories", text: $vm.calorieText, unit: "kcal")
                targetField("Protein", text: $vm.proteinText, unit: "g")
                targetField("Carbs", text: $vm.carbText, unit: "g")
                targetField("Fat", text: $vm.fatText, unit: "g")
                targetField("Fiber", text: $vm.fiberText, unit: "g")
                targetField("Steps", text: $vm.stepsText, unit: "")
                Button("Save targets") { vm.saveManualTargets() }
                Button("Recalculate from profile") { vm.recalcFromProfile() }
                    .foregroundStyle(Theme.accent)
            }

            Section("Units") {
                Picker("Units", selection: Binding(get: { vm.profile?.units ?? .metric },
                                                   set: { vm.setUnits($0) })) {
                    Text("Metric").tag(Units.metric); Text("Imperial").tag(Units.imperial)
                }.pickerStyle(.segmented)
            }

            Section("Sync & Health") {
                Toggle("Cloud sync (multi-device)", isOn: Binding(
                    get: { vm.profile?.cloudSyncEnabled ?? false },
                    set: { vm.setCloudSync($0) }))
                Toggle("Sync activity from Health", isOn: Binding(
                    get: { vm.profile?.healthSyncEnabled ?? false },
                    set: { on in Task { await vm.setHealthSync(on) } }))
                LabeledContent("Status") { ConnectivityPill(isOnline: env.reachability.isOnline) }
            }

            Section("Notifications") {
                Toggle("Meal logging reminders", isOn: Binding(
                    get: { vm.profile?.mealReminders ?? true }, set: { vm.setMealReminders($0) }))
                Toggle("Weigh-in reminders", isOn: Binding(
                    get: { vm.profile?.weighInReminders ?? true }, set: { vm.setWeighInReminders($0) }))
            }

            Section("Privacy") {
                Text("Your data is stored encrypted on this device (iOS Data Protection). Nothing is uploaded unless you enable Cloud sync. HealthKit data is read only with your permission.")
                    .font(.caption).foregroundStyle(.secondary)
                Button("Export my data") {
                    if let data = vm.exportData() { exportURL = writeTemp(data) }
                }
                Button("Delete account & data", role: .destructive) { showDeleteConfirm = true }
            }

            Section {
                LabeledContent("Version", value: "1.0.0")
            } footer: {
                Text("RecompCoach — evidence-based body recomposition. Guidance is informational, not medical advice.")
            }
        }
        .confirmationDialog("Delete everything?", isPresented: $showDeleteConfirm, titleVisibility: .visible) {
            Button("Delete all data", role: .destructive) { /* wipe store + keychain in production */ }
            Button("Cancel", role: .cancel) {}
        }
        .sheet(item: Binding(get: { exportURL.map { ExportFile(url: $0) } }, set: { _ in exportURL = nil })) { file in
            ShareSheet(items: [file.url])
        }
    }

    private func targetField(_ title: String, text: Binding<String>, unit: String) -> some View {
        HStack {
            Text(title); Spacer()
            TextField("0", text: text).keyboardType(.numberPad).multilineTextAlignment(.trailing).frame(width: 80)
            if !unit.isEmpty { Text(unit).foregroundStyle(.secondary) }
        }
    }

    private func writeTemp(_ data: Data) -> URL {
        let url = FileManager.default.temporaryDirectory.appending(path: "recompcoach-export.bin")
        try? data.write(to: url)
        return url
    }
}

struct ExportFile: Identifiable { let id = UUID(); let url: URL }

/// UIKit share sheet bridge for the encrypted export.
struct ShareSheet: UIViewControllerRepresentable {
    var items: [Any]
    func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: items, applicationActivities: nil)
    }
    func updateUIViewController(_ vc: UIActivityViewController, context: Context) {}
}

#Preview { SettingsView().environment(AppEnvironment.preview()) }
