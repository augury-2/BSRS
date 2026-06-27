import SwiftUI

struct ActivityView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var today = DailyActivity(steps: 0, distanceMeters: 0, activeEnergyKcal: 0, activeMinutes: 0)
    @State private var weekSteps: [(Date, Int)] = []
    @State private var workouts: [ActivityLog] = []
    @State private var stepsTarget = 10000
    @State private var showAdd = false

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                Card {
                    HStack {
                        StatTile(systemImage: "figure.walk", title: "Steps", value: today.steps.formatted(), tint: Theme.steps)
                        StatTile(systemImage: "map", title: "Distance", value: String(format: "%.2f km", today.distanceMeters/1000), tint: Theme.accent)
                    }
                }
                Card {
                    HStack {
                        StatTile(systemImage: "flame.fill", title: "Active energy", value: "\(Int(today.activeEnergyKcal)) kcal", tint: Theme.protein)
                        StatTile(systemImage: "timer", title: "Active min", value: "\(today.activeMinutes)", tint: Theme.fiber)
                    }
                }
                Card {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Steps this week").font(.subheadline.bold())
                        StepsBarChart(points: weekSteps, target: stepsTarget)
                    }
                }
                Card {
                    VStack(alignment: .leading, spacing: 10) {
                        HStack { Text("Workouts").font(.subheadline.bold()); Spacer()
                            Button { showAdd = true } label: { Label("Add", systemImage: "plus") }.font(.caption) }
                        if workouts.isEmpty {
                            Text("No workouts logged today.").font(.caption).foregroundStyle(.secondary)
                        }
                        ForEach(workouts) { w in
                            HStack {
                                Image(systemName: "figure.strengthtraining.traditional").foregroundStyle(Theme.protein)
                                VStack(alignment: .leading) {
                                    Text(w.name)
                                    if let d = w.durationMinutes { Text("\(Int(d)) min").font(.caption).foregroundStyle(.secondary) }
                                }
                                Spacer()
                                Text("\(Int(w.energyKcal)) kcal").font(.caption).foregroundStyle(.secondary)
                            }
                        }
                    }
                }
            }.padding()
        }
        .navigationTitle("Activity")
        .sheet(isPresented: $showAdd) { AddWorkoutSheet { load() } }
        .task { await refresh() }
    }

    private func refresh() async {
        if env.store.currentProfile()?.healthSyncEnabled == true {
            today = await env.activity.todaysActivity()
        }
        load()
    }
    private func load() {
        stepsTarget = env.store.currentProfile()?.targets?.steps ?? 10000
        if let log = env.store.activity(on: .now).first(where: { $0.kind == .steps }) {
            today = DailyActivity(steps: log.steps ?? today.steps,
                                  distanceMeters: log.distanceMeters ?? today.distanceMeters,
                                  activeEnergyKcal: log.energyKcal,
                                  activeMinutes: log.activeMinutes ?? today.activeMinutes)
        }
        workouts = env.store.activity(on: .now).filter { $0.kind != .steps }
        let from = Calendar.current.date(byAdding: .day, value: -6, to: .now)!
        weekSteps = env.store.activity(in: from...Date()).filter { $0.kind == .steps }
            .compactMap { a in a.steps.map { (a.date, $0) } }
    }
}

#Preview { NavigationStack { ActivityView() }.environment(AppEnvironment.preview()) }
