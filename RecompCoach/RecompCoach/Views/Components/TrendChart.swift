import SwiftUI
import Charts

/// A simple line+point trend chart for a dated numeric series (Swift Charts).
struct TrendChart: View {
    struct Point: Identifiable { let id = UUID(); let date: Date; let value: Double }
    var points: [Point]
    var color: Color
    var unit: String
    var showPoints: Bool = true

    var body: some View {
        if points.isEmpty {
            ContentUnavailableView("No data yet", systemImage: "chart.xyaxis.line",
                                   description: Text("Log entries to see your trend."))
                .frame(height: 180)
        } else {
            Chart(points) { p in
                LineMark(x: .value("Date", p.date), y: .value(unit, p.value))
                    .interpolationMethod(.catmullRom)
                    .foregroundStyle(color)
                if showPoints {
                    PointMark(x: .value("Date", p.date), y: .value(unit, p.value))
                        .foregroundStyle(color)
                }
                AreaMark(x: .value("Date", p.date), y: .value(unit, p.value))
                    .interpolationMethod(.catmullRom)
                    .foregroundStyle(LinearGradient(colors: [color.opacity(0.25), .clear],
                                                    startPoint: .top, endPoint: .bottom))
            }
            .chartYScale(domain: .automatic(includesZero: false))
            .frame(height: 180)
        }
    }

    init(_ pairs: [(Date, Double)], color: Color, unit: String, showPoints: Bool = true) {
        self.points = pairs.map { Point(date: $0.0, value: $0.1) }
        self.color = color
        self.unit = unit
        self.showPoints = showPoints
    }
}

/// Bar chart for steps over the week.
struct StepsBarChart: View {
    var points: [(Date, Int)]
    var target: Int

    var body: some View {
        Chart {
            ForEach(points, id: \.0) { (date, steps) in
                BarMark(x: .value("Day", date, unit: .day),
                        y: .value("Steps", steps))
                    .foregroundStyle(steps >= target ? Theme.fiber : Theme.steps)
                    .cornerRadius(5)
            }
            RuleMark(y: .value("Target", target))
                .lineStyle(StrokeStyle(lineWidth: 1, dash: [4]))
                .foregroundStyle(.secondary)
        }
        .frame(height: 160)
    }
}
