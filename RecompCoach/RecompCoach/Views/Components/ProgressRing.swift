import SwiftUI

/// A circular progress ring with a centered label. Used for calories & steps.
struct ProgressRing: View {
    var progress: Double            // 0...1 (values >1 wrap visually capped)
    var color: Color
    var lineWidth: CGFloat = 12
    var size: CGFloat = 120
    var title: String
    var value: String
    var subtitle: String

    var body: some View {
        ZStack {
            Circle()
                .stroke(color.opacity(0.18), lineWidth: lineWidth)
            Circle()
                .trim(from: 0, to: max(0.001, min(progress, 1)))
                .stroke(color, style: StrokeStyle(lineWidth: lineWidth, lineCap: .round))
                .rotationEffect(.degrees(-90))
                .animation(.easeInOut(duration: 0.5), value: progress)
            VStack(spacing: 2) {
                Text(value).font(.title2.bold()).monospacedDigit()
                Text(subtitle).font(.caption2).foregroundStyle(.secondary)
            }
        }
        .frame(width: size, height: size)
        .accessibilityElement(children: .ignore)
        .accessibilityLabel("\(title): \(value) \(subtitle)")
    }
}

#Preview {
    HStack {
        ProgressRing(progress: 0.62, color: Theme.accent, title: "Calories",
                     value: "1,310", subtitle: "of 2,100")
        ProgressRing(progress: 0.74, color: Theme.steps, title: "Steps",
                     value: "7.4k", subtitle: "of 10k")
    }.padding()
}
