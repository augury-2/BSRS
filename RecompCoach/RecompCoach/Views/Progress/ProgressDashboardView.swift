import SwiftUI

struct ProgressDashboardView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var vm: ProgressViewModel?
    @State private var showAdd = false

    var body: some View {
        NavigationStack {
            Group {
                if let vm { content(vm) }
                else { ProgressView().task { let v = ProgressViewModel(store: env.store); v.load(); vm = v } }
            }
            .navigationTitle("Progress")
            .toolbar { ToolbarItem(placement: .topBarTrailing) {
                Button { showAdd = true } label: { Image(systemName: "plus") } } }
            .sheet(isPresented: $showAdd) { AddMeasurementSheet { vm?.load() } }
        }
    }

    @ViewBuilder
    private func content(_ vm: ProgressViewModel) -> some View {
        ScrollView {
            VStack(spacing: 16) {
                trendBanner(vm)
                chartCard(vm, title: "Weight", series: vm.series(\.weightKg), unit: "kg", color: Theme.accent)
                chartCard(vm, title: "Waist", series: vm.series(\.waistCm), unit: "cm", color: Theme.carbs)
                chartCard(vm, title: "Body fat", series: vm.series(\.bodyFatPercent), unit: "%", color: Theme.protein)
                insightsCard(vm)
                historyCard(vm)
            }.padding()
        }
        .refreshable { vm.load() }
    }

    private func trendBanner(_ vm: ProgressViewModel) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 6) {
                Text("Trend").font(.caption).foregroundStyle(.secondary)
                Text(vm.trendSummary.isEmpty ? "Log measurements to see your trend" : vm.trendSummary)
                    .font(.headline)
                if let s = vm.snapshot {
                    Text(String(format: "%+.2f kg/wk · waist %@",
                                s.weightChangeKgPerWeek,
                                s.waistChangeCmPerWeek.map { String(format: "%+.1f cm/wk", $0) } ?? "—"))
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
        }
    }

    private func chartCard(_ vm: ProgressViewModel, title: String, series: [(Date, Double)], unit: String, color: Color) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 8) {
                Text(title).font(.subheadline.bold())
                TrendChart(series, color: color, unit: unit)
            }
        }
    }

    private func insightsCard(_ vm: ProgressViewModel) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 10) {
                HStack { Text("Coach insights").font(.subheadline.bold()); Spacer()
                    NavigationLink { CoachView() } label: { Text("Ask coach").font(.caption) } }
                ForEach(vm.insights.prefix(4)) { InsightCard(insight: $0, expanded: true) }
            }
        }
    }

    private func historyCard(_ vm: ProgressViewModel) -> some View {
        Card {
            VStack(alignment: .leading, spacing: 8) {
                Text("History").font(.subheadline.bold())
                ForEach(vm.measurements.reversed()) { m in
                    HStack {
                        Text(m.date.formatted(date: .abbreviated, time: .omitted)).font(.caption)
                        Spacer()
                        if let w = m.weightKg { Text("\(w.clean) kg").font(.caption) }
                        if let waist = m.waistCm { Text("· \(waist.clean) cm").font(.caption).foregroundStyle(.secondary) }
                    }
                    .swipeActions { Button("Delete", role: .destructive) { vm.delete(m) } }
                }
            }
        }
    }
}

#Preview { ProgressDashboardView().environment(AppEnvironment.preview()) }
