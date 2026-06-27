import Foundation

/// Computes evidence-based daily targets from a user profile.
///
/// Energy: Mifflin–St Jeor BMR (or Katch–McArdle when lean mass is known),
/// scaled by an activity multiplier, then goal-adjusted.
/// Protein: lean-mass-aware g/kg (Helms et al.; ISSN position stand).
/// Fiber: 14 g per 1000 kcal (IOM/ACSM). Micros: adult DRIs by sex.
struct TargetsEngine {

    struct Result {
        var bmr: Double
        var tdee: Double
        var targets: NutritionTargets
    }

    static func compute(for p: UserProfile) -> Result {
        let bmr = basalMetabolicRate(for: p)
        let tdee = bmr * p.activity.multiplier
        var calories = tdee * (1 + p.goal.calorieAdjustment)

        // Safety floor so deficits never go unhealthily low.
        let minCalories = p.sex == .male ? 1500.0 : 1200.0
        calories = max(calories, minCalories)
        if let override = p.manualCalorieOverride { calories = override }
        calories = (calories / 10).rounded() * 10   // round to nearest 10 kcal

        // Protein — lean-mass aware when body fat is known.
        var protein: Double
        if let lbm = p.leanMassKg {
            protein = 2.8 * lbm                      // ~2.3–3.1 g/kg LBM in a deficit
        } else {
            let gPerKg: Double = (p.goal == .maintain) ? 1.8 : 2.2
            protein = gPerKg * p.currentWeightKg
        }
        if let override = p.manualProteinOverride { protein = override }
        protein = protein.rounded()

        // Fat — floor at 0.5 g/kg to protect hormones; default 0.8 g/kg.
        let fat = max(0.5, 0.8) * p.currentWeightKg
        let fatRounded = fat.rounded()

        // Carbs — remaining energy.
        let proteinKcal = protein * 4
        let fatKcal = fatRounded * 9
        let carbs = max(0, (calories - proteinKcal - fatKcal) / 4).rounded()

        // Fiber — 14 g per 1000 kcal.
        let fiber = (14 * calories / 1000).rounded()

        // Steps — recomposition favors high NEAT.
        let steps = p.goal == .maintain ? 8000 : 10000

        let targets = NutritionTargets(
            calories: calories,
            protein: protein,
            carbs: carbs,
            fat: fatRounded,
            fiber: fiber,
            steps: steps,
            micros: microRDAs(for: p)
        )
        return Result(bmr: bmr.rounded(), tdee: tdee.rounded(), targets: targets)
    }

    /// Mifflin–St Jeor, or Katch–McArdle when lean mass is available (more
    /// individualized for lifters with a known body-fat %).
    static func basalMetabolicRate(for p: UserProfile) -> Double {
        if let lbm = p.leanMassKg {
            return 370 + 21.6 * lbm
        }
        let base = 10 * p.currentWeightKg + 6.25 * p.heightCm - 5 * Double(p.age)
        return base + (p.sex == .male ? 5 : -161)
    }

    /// Adult Dietary Reference Intakes (ages 19–50). Values chosen from
    /// IOM/NIH references; vegetarian iron needs trend higher in practice.
    static func microRDAs(for p: UserProfile) -> [NutrientKey: Double] {
        let male = p.sex == .male
        return [
            .vitA:      male ? 900 : 700,    // mcg RAE
            .vitC:      male ? 90  : 75,      // mg
            .vitD:      15,                   // mcg (600 IU)
            .vitE:      15,                   // mg
            .vitK:      male ? 120 : 90,      // mcg
            .b1:        male ? 1.2 : 1.1,     // mg
            .b2:        male ? 1.3 : 1.1,     // mg
            .b3:        male ? 16  : 14,      // mg
            .b6:        1.3,                  // mg
            .folate:    400,                  // mcg
            .b12:       2.4,                  // mcg
            .calcium:   1000,                 // mg
            .iron:      male ? 8   : 18,      // mg
            .magnesium: male ? 400 : 310,     // mg
            .potassium: male ? 3400 : 2600,   // mg
            .sodium:    2300,                 // mg (upper guidance)
            .zinc:      male ? 11  : 8         // mg
        ]
    }
}
