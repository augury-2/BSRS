import SwiftUI

/// Micronutrient radar (spider) chart drawn with Canvas. Each axis is a
/// nutrient; the filled polygon is % of RDA (clamped to 150% for display).
struct RadarChartView: View {
    /// (nutrient, percentOfRDA) pairs.
    var data: [(NutrientKey, Double)]
    var maxValue: Double = 150
    var color: Color = Theme.accent

    var body: some View {
        Canvas { ctx, size in
            let count = data.count
            guard count >= 3 else { return }
            let center = CGPoint(x: size.width / 2, y: size.height / 2)
            let radius = min(size.width, size.height) / 2 - 26

            // Grid rings at 50 / 100 / 150 %.
            for ring in [0.33, 0.66, 1.0] {
                var path = Path()
                for i in 0..<count {
                    let pt = vertex(i: i, count: count, center: center, radius: radius * ring)
                    if i == 0 { path.move(to: pt) } else { path.addLine(to: pt) }
                }
                path.closeSubpath()
                ctx.stroke(path, with: .color(.secondary.opacity(0.25)), lineWidth: 1)
            }

            // Spokes + labels.
            for i in 0..<count {
                let outer = vertex(i: i, count: count, center: center, radius: radius)
                var spoke = Path(); spoke.move(to: center); spoke.addLine(to: outer)
                ctx.stroke(spoke, with: .color(.secondary.opacity(0.2)), lineWidth: 1)

                let labelPt = vertex(i: i, count: count, center: center, radius: radius + 14)
                let text = Text(data[i].0.displayName).font(.system(size: 9)).foregroundColor(.secondary)
                ctx.draw(text, at: labelPt)
            }

            // Data polygon.
            var poly = Path()
            for i in 0..<count {
                let ratio = min(data[i].1, maxValue) / maxValue
                let pt = vertex(i: i, count: count, center: center, radius: radius * ratio)
                if i == 0 { poly.move(to: pt) } else { poly.addLine(to: pt) }
            }
            poly.closeSubpath()
            ctx.fill(poly, with: .color(color.opacity(0.28)))
            ctx.stroke(poly, with: .color(color), lineWidth: 2)
        }
        .frame(height: 240)
        .accessibilityLabel("Micronutrient radar chart")
    }

    private func vertex(i: Int, count: Int, center: CGPoint, radius: CGFloat) -> CGPoint {
        let angle = (Double(i) / Double(count)) * 2 * .pi - .pi / 2
        return CGPoint(x: center.x + radius * cos(angle), y: center.y + radius * sin(angle))
    }
}

#Preview {
    RadarChartView(data: [(.iron, 120), (.calcium, 80), (.magnesium, 95),
                          (.potassium, 60), (.zinc, 110), (.b12, 140),
                          (.vitD, 40), (.vitC, 130)])
        .padding()
}
