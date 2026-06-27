import Foundation

/// Pure functions for aggregating logged nutrition and estimating energy
/// balance. No side effects → trivially unit-testable and fully offline.
struct NutritionCalculator {

    /// Sum a set of diary entries into a single `Nutrients`.
    static func totals(_ entries: [NutritionEntry]) -> Nutrients {
        Nutrients.sum(entries.map { $0.nutrients })
    }

    /// Sum entries grouped per meal.
    static func totalsByMeal(_ entries: [NutritionEntry]) -> [MealType: Nutrients] {
        var out: [MealType: Nutrients] = [:]
        for e in entries { out[e.meal, default: .zero] += e.nutrients }
        return out
    }

    /// % of daily reference intake for each tracked nutrient.
    static func percentRDA(_ consumed: Nutrients, targets: NutritionTargets) -> [NutrientKey: Double] {
        var out: [NutrientKey: Double] = [:]
        for key in NutrientKey.allCases where key.isMicro {
            guard let rda = targets.micros[key], rda > 0 else { continue }
            out[key] = consumed[key] / rda * 100
        }
        return out
    }

    /// "High in / low in" highlights for the Build-My-Diet screen.
    static func highlights(_ consumed: Nutrients, targets: NutritionTargets) -> (high: [NutrientKey], low: [NutrientKey]) {
        let pct = percentRDA(consumed, targets: targets)
        let high = pct.filter { $0.value >= 100 }.map(\.key)
        let low  = pct.filter { $0.value < 50 }.map(\.key)
        // Stable ordering by radar priority then name.
        func sort(_ a: [NutrientKey]) -> [NutrientKey] {
            a.sorted { ($0.displayName) < ($1.displayName) }
        }
        return (sort(high), sort(low))
    }

    // MARK: - Energy balance

    /// Rough energy burned from steps. ~0.0005 kcal per step per kg bodyweight
    /// (≈0.04 kcal/step at 80 kg) — a widely used field approximation.
    static func energyFromSteps(_ steps: Int, weightKg: Double) -> Double {
        Double(steps) * 0.0005 * weightKg
    }

    /// Estimated total calories out for the day:
    /// resting (BMR) + active energy (HealthKit if available, else step+workout estimate).
    static func caloriesOut(bmr: Double,
                            activeEnergyKcal: Double?,
                            steps: Int,
                            workoutKcal: Double,
                            weightKg: Double) -> Double {
        if let active = activeEnergyKcal, active > 0 {
            return bmr + active
        }
        return bmr + energyFromSteps(steps, weightKg: weightKg) + workoutKcal
    }

    /// calories in − calories out (negative = deficit).
    static func energyBalance(caloriesIn: Double, caloriesOut: Double) -> Double {
        caloriesIn - caloriesOut
    }

    // MARK: - Approximate workout energy (manual logging fallback)

    /// METs-based estimate: kcal = MET * 3.5 * kg / 200 * minutes.
    static func workoutEnergy(met: Double, minutes: Double, weightKg: Double) -> Double {
        met * 3.5 * weightKg / 200.0 * minutes
    }
}
