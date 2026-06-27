import SwiftUI

/// Horizontal macro progress bar: label, value/target, colored fill.
struct MacroBar: View {
    var title: String
    var value: Double
    var target: Double
    var unit: String
    var color: Color

    private var progress: Double { target > 0 ? min(value / target, 1) : 0 }
    private var over: Bool { value > target * 1.05 }

    var body: some View {
        VStack(alignment: .leading, spacing: 5) {
            HStack {
                Text(title).font(.subheadline.weight(.semibold))
                Spacer()
                Text("\(value.clean) / \(target.clean) \(unit)")
                    .font(.caption).monospacedDigit()
                    .foregroundStyle(over ? Theme.protein : .secondary)
            }
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule().fill(color.opacity(0.18))
                    Capsule().fill(color)
                        .frame(width: max(4, geo.size.width * progress))
                        .animation(.easeInOut(duration: 0.4), value: progress)
                }
            }
            .frame(height: 9)
        }
    }
}

/// Compact labeled stat used on the dashboard (steps, distance, balance...).
struct StatTile: View {
    var systemImage: String
    var title: String
    var value: String
    var tint: Color = Theme.accent

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: systemImage)
                .font(.title3)
                .foregroundStyle(tint)
                .frame(width: 36, height: 36)
                .background(tint.opacity(0.15), in: RoundedRectangle(cornerRadius: 10))
            VStack(alignment: .leading, spacing: 1) {
                Text(value).font(.headline).monospacedDigit()
                Text(title).font(.caption).foregroundStyle(.secondary)
            }
            Spacer()
        }
    }
}
