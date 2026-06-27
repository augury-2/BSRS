import Foundation

/// Populates an in-memory store for previews & tests.
@MainActor
enum PreviewSeed {
    static func populate(_ store: AppStore) {
        let profile = UserProfile(name: "Alex", age: 28, sex: .male, heightCm: 174,
                                  currentWeightKg: 81, goal: .loseFatGainMuscle,
                                  activity: .moderate, trainingDaysPerWeek: 5,
                                  bodyFatPercent: 22)
        profile.targets = TargetsEngine.compute(for: profile).targets
        store.saveProfile(profile)

        let whey = store.upsertCustomFood(name: "Whey Protein",
            servingGrams: 30,
            per100g: Nutrients([.calories: 380, .protein: 80, .carbs: 8, .fat: 6, .fiber: 0,
                                .calcium: 500, .b12: 2, .sodium: 300]))
        let paneer = store.upsertCustomFood(name: "Paneer (low-fat)",
            servingGrams: 100,
            per100g: Nutrients([.calories: 150, .protein: 18, .carbs: 4, .fat: 8, .fiber: 0,
                                .calcium: 480, .iron: 0.3]))
        store.addEntry(food: whey, grams: 30, meal: .breakfast, date: .now)
        store.addEntry(food: paneer, grams: 150, meal: .lunch, date: .now)

        // A short measurement history for the chart.
        let cal = Calendar.current
        let weights = [81.4, 81.0, 80.5, 80.1, 79.6]
        let waists  = [88.0, 87.6, 87.1, 86.8, 86.2]
        for (i, _) in weights.enumerated() {
            let date = cal.date(byAdding: .day, value: -7 * (weights.count - 1 - i), to: .now)!
            store.addMeasurement(BodyMeasurement(date: date, weightKg: weights[i], waistCm: waists[i]))
        }
        store.upsertSteps(7421, distanceMeters: 5320, activeMinutes: 38, activeEnergy: 410, on: .now)
    }
}
