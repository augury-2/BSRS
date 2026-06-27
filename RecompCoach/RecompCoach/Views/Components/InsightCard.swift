import SwiftUI

struct InsightCard: View {
    var insight: CoachingInsight
    var expanded: Bool = false

    private var tint: Color {
        switch insight.severity {
        case .positive: return Theme.fiber
        case .info:     return Theme.accent
        case .warning:  return Theme.carbs
        case .action:   return Theme.protein
        }
    }

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: insight.severity.systemImage)
                .foregroundStyle(tint)
                .font(.title3)
            VStack(alignment: .leading, spacing: 4) {
                Text(insight.title).font(.subheadline.bold())
                Text(insight.message).font(.subheadline).foregroundStyle(.primary)
                if expanded {
                    Text(insight.rationale)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .padding(.top, 2)
                }
            }
            Spacer(minLength: 0)
        }
        .padding(14)
        .background(tint.opacity(0.10), in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 14).strokeBorder(tint.opacity(0.25)))
    }
}

/// Pill that shows offline/online state.
struct ConnectivityPill: View {
    var isOnline: Bool
    var body: some View {
        Label(isOnline ? "Online" : "Offline",
              systemImage: isOnline ? "wifi" : "wifi.slash")
            .font(.caption2.weight(.semibold))
            .padding(.horizontal, 10).padding(.vertical, 4)
            .background((isOnline ? Theme.fiber : Color.secondary).opacity(0.18), in: Capsule())
            .foregroundStyle(isOnline ? Theme.fiber : .secondary)
    }
}
