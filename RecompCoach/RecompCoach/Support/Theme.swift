import SwiftUI

/// Central design tokens. Works in light & dark mode via system materials and
/// semantic colors.
enum Theme {
    static let accent = Color(red: 0.05, green: 0.65, blue: 0.64)   // teal
    static let protein = Color(red: 0.91, green: 0.30, blue: 0.39)  // red
    static let carbs = Color(red: 0.97, green: 0.62, blue: 0.18)    // amber
    static let fat = Color(red: 0.39, green: 0.45, blue: 0.95)      // indigo
    static let fiber = Color(red: 0.30, green: 0.73, blue: 0.42)    // green
    static let steps = Color(red: 0.49, green: 0.36, blue: 0.93)    // purple

    static let cardCorner: CGFloat = 18
    static let cardPadding: CGFloat = 16

    static func color(for key: NutrientKey) -> Color {
        switch key {
        case .protein: return protein
        case .carbs:   return carbs
        case .fat:     return fat
        case .fiber:   return fiber
        default:       return accent
        }
    }
}

/// Reusable card container.
struct Card<Content: View>: View {
    @ViewBuilder var content: Content
    var body: some View {
        content
            .padding(Theme.cardPadding)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.regularMaterial, in: RoundedRectangle(cornerRadius: Theme.cardCorner, style: .continuous))
    }
}

extension Double {
    var clean: String {
        self == rounded() ? String(Int(self)) : String(format: "%.1f", self)
    }
}
