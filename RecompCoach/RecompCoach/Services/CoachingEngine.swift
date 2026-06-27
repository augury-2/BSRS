import Foundation

/// Snapshot of a user's week, fed into the coaching engine. Mirrors the
/// `context` object sent to the optional online AI coach so both reason over
/// identical data.
struct WeeklySnapshot: Codable, Equatable {
    var goal: GoalType
    var bodyWeightKg: Double
    var weightChangeKgPerWeek: Double      // negative = losing
    var waistChangeCmPerWeek: Double?      // negative = shrinking
    var avgCalories: Double
    var calorieTarget: Double
    var avgProtein: Double
    var proteinTarget: Double
    var avgFiber: Double
    var fiberTarget: Double
    var avgSteps: Int
    var stepsTarget: Int
    var trainingDaysPerWeek: Int
    var loggingDays: Int                   // days with at least one entry this week
    var reportedLowEnergy: Bool
    var avgSleepHours: Double?
}

enum InsightSeverity: String, Codable {
    case positive, info, warning, action
    var systemImage: String {
        switch self {
        case .positive: return "checkmark.seal.fill"
        case .info:     return "info.circle.fill"
        case .warning:  return "exclamationmark.triangle.fill"
        case .action:   return "bolt.fill"
        }
    }
}

struct CoachingInsight: Identifiable, Codable, Equatable {
    var id = UUID()
    var severity: InsightSeverity
    var title: String
    var message: String
    var rationale: String      // the "why", in plain language
}

/// Deterministic, offline, evidence-based coaching. Pure function of the
/// snapshot → ordered insights (most actionable first).
struct CoachingEngine {

    static func analyze(_ s: WeeklySnapshot) -> [CoachingInsight] {
        var out: [CoachingInsight] = []

        // 0. Adherence gate — without data we can't coach trends.
        if s.loggingDays < 4 {
            out.append(.init(
                severity: .info,
                title: "Log a little more this week",
                message: "You logged \(s.loggingDays) of 7 days. Aim for 5+ so the coach can read real trends.",
                rationale: "Trend-based decisions need consistent data; a few logged days can mislead adjustments."))
        }

        // 1. Rate of weight change vs goal.
        let lossPctPerWeek = -s.weightChangeKgPerWeek / max(s.bodyWeightKg, 1) * 100
        let waistShrinking = (s.waistChangeCmPerWeek ?? 0) < -0.1

        switch s.goal {
        case .loseFatMaintainMuscle, .loseFatGainMuscle:
            if lossPctPerWeek > 1.0 {
                out.append(.init(
                    severity: .warning,
                    title: "You're losing weight too fast",
                    message: "Add ~150 kcal/day (ideally carbs around training). Target 0.5–1.0% of bodyweight per week.",
                    rationale: "Faster-than-1%/week loss increasingly sacrifices lean mass and performance (Garthe 2011; Helms 2014)."))
            } else if lossPctPerWeek >= 0.4 {
                out.append(.init(
                    severity: .positive,
                    title: "Ideal fat-loss pace",
                    message: "About \(String(format: "%.1f", lossPctPerWeek))%/week — keep everything the same.",
                    rationale: "0.5–1.0%/week maximizes fat loss while sparing muscle."))
            } else if lossPctPerWeek > 0 || waistShrinking {
                out.append(.init(
                    severity: .positive,
                    title: "Recomposition in progress",
                    message: waistShrinking
                        ? "Scale barely moved but your waist is shrinking — you're losing fat while holding muscle."
                        : "Slow, steady loss. If you'd like it faster, add ~1,500 steps/day before cutting calories.",
                    rationale: "Stable weight with a shrinking waist is the classic signature of recomposition."))
            } else {
                // Stall / gaining while in a fat-loss goal.
                out.append(.init(
                    severity: .action,
                    title: "Fat loss has stalled",
                    message: "First confirm logging is accurate. Then add ~2,000 steps/day; if still flat after a week, trim ~150 kcal.",
                    rationale: "Move NEAT before cutting calories — it preserves training performance and muscle."))
            }
        case .maintain:
            if abs(lossPctPerWeek) <= 0.3 {
                out.append(.init(
                    severity: .positive,
                    title: "Bodyweight stable",
                    message: "You're holding maintenance well.",
                    rationale: "±0.3%/week is normal fluctuation around maintenance."))
            } else if lossPctPerWeek > 0.3 {
                out.append(.init(
                    severity: .info,
                    title: "Trending down",
                    message: "Add ~150–200 kcal/day if you intended to maintain.",
                    rationale: "A persistent drop means you're slightly under maintenance."))
            } else {
                out.append(.init(
                    severity: .info,
                    title: "Trending up",
                    message: "Trim ~150 kcal/day or add steps if you intended to maintain.",
                    rationale: "A persistent rise means you're slightly over maintenance."))
            }
        }

        // 2. Protein — the #1 muscle-retention lever.
        if s.avgProtein < s.proteinTarget * 0.9 {
            out.append(.init(
                severity: .action,
                title: "Hit your protein",
                message: "Averaging \(Int(s.avgProtein)) g vs \(Int(s.proteinTarget)) g target. Add a whey shake or extra paneer/tofu/dal.",
                rationale: "Adequate protein (~1.6–2.2 g/kg, higher in a deficit) is the strongest dietary driver of muscle retention (Morton 2018; Helms 2014)."))
        } else {
            out.append(.init(
                severity: .positive,
                title: "Protein on point",
                message: "Averaging \(Int(s.avgProtein)) g/day — great for protecting muscle.",
                rationale: "Meeting protein targets is the top priority for recomposition."))
        }

        // 3. Fiber.
        if s.avgFiber < s.fiberTarget * 0.8 {
            out.append(.init(
                severity: .info,
                title: "Add more fiber",
                message: "Averaging \(Int(s.avgFiber)) g vs \(Int(s.fiberTarget)) g. Add vegetables, legumes, oats or berries.",
                rationale: "Fiber improves satiety and gut health and helps adherence in a deficit (IOM: ~14 g/1000 kcal)."))
        }

        // 4. Steps / NEAT.
        if s.avgSteps < Int(Double(s.stepsTarget) * 0.7) {
            out.append(.init(
                severity: .info,
                title: "Bump your daily steps",
                message: "Averaging \(s.avgSteps.formatted()) vs \(s.stepsTarget.formatted()). Walking is the cheapest, lowest-fatigue fat-loss tool.",
                rationale: "NEAT is a large, adjustable part of daily energy expenditure and doesn't impair recovery like extra cardio can."))
        }

        // 5. Calorie adherence vs result.
        if s.avgCalories > s.calorieTarget * 1.1 && lossPctPerWeek <= 0 &&
            (s.goal == .loseFatMaintainMuscle || s.goal == .loseFatGainMuscle) {
            out.append(.init(
                severity: .warning,
                title: "Intake is above target",
                message: "Averaging \(Int(s.avgCalories)) kcal vs \(Int(s.calorieTarget)). Tighten portions/logging before changing the plan.",
                rationale: "Most stalls are an energy-intake accounting issue, not a metabolic one."))
        }

        // 6. Energy / sleep.
        if s.reportedLowEnergy {
            out.append(.init(
                severity: .action,
                title: "Boost energy & recovery",
                message: "Put more carbs around training and prioritize 7–9 h sleep.",
                rationale: "Carbohydrate availability supports training output; sleep loss worsens muscle retention and hunger (Nedeltcheva 2010)."))
        }
        if let sleep = s.avgSleepHours, sleep < 7 {
            out.append(.init(
                severity: .info,
                title: "Aim for more sleep",
                message: "Averaging \(String(format: "%.1f", sleep)) h. Target 7–9 h.",
                rationale: "Short sleep increases lean-mass loss and appetite during a deficit."))
        }

        // Order: action → warning → info → positive.
        let rank: [InsightSeverity: Int] = [.action: 0, .warning: 1, .info: 2, .positive: 3]
        return out.sorted { (rank[$0.severity] ?? 9) < (rank[$1.severity] ?? 9) }
    }

    /// One-line trend classification used on the Progress tab.
    static func classifyTrend(weightChangeKgPerWeek: Double,
                              waistChangeCmPerWeek: Double?,
                              bodyWeightKg: Double) -> String {
        let lossPct = -weightChangeKgPerWeek / max(bodyWeightKg, 1) * 100
        let waistDown = (waistChangeCmPerWeek ?? 0) < -0.1
        if abs(lossPct) < 0.2 && waistDown { return "Losing fat while maintaining muscle" }
        if lossPct >= 0.4 { return "In a calorie deficit — losing weight" }
        if lossPct <= -0.4 { return "In a calorie surplus — gaining weight" }
        return "Roughly maintaining" + (waistDown ? " (waist still shrinking)" : "")
    }
}
