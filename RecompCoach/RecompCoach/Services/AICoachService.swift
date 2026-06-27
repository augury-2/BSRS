import Foundation

/// Optional online AI coach. When offline (or sync disabled) it returns the
/// best matching rules-based insight so the user always gets an answer.
@MainActor
final class AICoachService {
    private let api: APIClienting
    private let reachability: Reachability
    init(api: APIClienting, reachability: Reachability) {
        self.api = api
        self.reachability = reachability
    }

    var isOnline: Bool { reachability.isOnline }

    func ask(_ question: String, history: [ChatMessage], snapshot: WeeklySnapshot) async -> ChatMessage {
        if reachability.isOnline {
            do {
                let reply = try await api.coachChat(
                    messages: history + [ChatMessage(role: .user, content: question)],
                    context: snapshot)
                return ChatMessage(role: .assistant, content: reply)
            } catch {
                // fall through to offline answer
            }
        }
        return ChatMessage(role: .assistant, content: offlineAnswer(for: question, snapshot: snapshot))
    }

    /// Deterministic offline fallback built from the rules engine + keyword match.
    private func offlineAnswer(for question: String, snapshot: WeeklySnapshot) -> String {
        let q = question.lowercased()
        let insights = CoachingEngine.analyze(snapshot)

        func find(_ keywords: [String]) -> CoachingInsight? {
            insights.first { ins in
                keywords.contains { q.contains($0) } &&
                (ins.title + ins.message).lowercased().contains(where: { _ in true })
            }
        }

        if q.contains("protein") {
            return "Target ~\(Int(snapshot.proteinTarget)) g/day (about 1.6–2.2 g/kg, higher while dieting). You're averaging \(Int(snapshot.avgProtein)) g. Protein is the #1 lever for keeping muscle in a deficit."
        }
        if q.contains("plateau") || q.contains("stall") || q.contains("not losing") {
            return "First verify logging is accurate. Then add ~2,000 steps/day; if still flat after a week, trim ~150 kcal from carbs or fat (never protein). A planned diet break can also restart progress."
        }
        if q.contains("fiber") {
            return "Aim for ~\(Int(snapshot.fiberTarget)) g/day from vegetables, legumes, oats and fruit. You're at ~\(Int(snapshot.avgFiber)) g."
        }
        if let top = insights.first {
            return "\(top.message)\n\nWhy: \(top.rationale)\n\n(Offline answer — connect to the internet for detailed Q&A.)"
        }
        return "I'm offline right now, but your plan looks on track. Connect to the internet for a detailed answer."
    }
}
