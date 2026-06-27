import Foundation

/// All trackable nutrients. Backed by a dictionary so summing, scaling and
/// iterating (e.g. for the micronutrient radar) is uniform and extensible.
enum NutrientKey: String, Codable, CaseIterable, Identifiable {
    // Macros + energy
    case calories, protein, carbs, fat, fiber, sugar, satFat
    // Vitamins
    case vitA, vitC, vitD, vitE, vitK, b1, b2, b3, b6, folate, b12
    // Minerals
    case calcium, iron, magnesium, potassium, sodium, zinc

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .calories: return "Calories"
        case .protein:  return "Protein"
        case .carbs:    return "Carbs"
        case .fat:      return "Fat"
        case .fiber:    return "Fiber"
        case .sugar:    return "Sugar"
        case .satFat:   return "Sat. Fat"
        case .vitA:     return "Vitamin A"
        case .vitC:     return "Vitamin C"
        case .vitD:     return "Vitamin D"
        case .vitE:     return "Vitamin E"
        case .vitK:     return "Vitamin K"
        case .b1:       return "Vitamin B1"
        case .b2:       return "Vitamin B2"
        case .b3:       return "Vitamin B3"
        case .b6:       return "Vitamin B6"
        case .folate:   return "Folate"
        case .b12:      return "Vitamin B12"
        case .calcium:  return "Calcium"
        case .iron:     return "Iron"
        case .magnesium:return "Magnesium"
        case .potassium:return "Potassium"
        case .sodium:   return "Sodium"
        case .zinc:     return "Zinc"
        }
    }

    var unit: String {
        switch self {
        case .calories: return "kcal"
        case .protein, .carbs, .fat, .fiber, .sugar, .satFat: return "g"
        case .vitA, .vitK, .folate, .b12, .vitD: return "mcg"
        case .vitC, .vitE, .b1, .b2, .b3, .b6,
             .calcium, .iron, .magnesium, .potassium, .sodium, .zinc: return "mg"
        }
    }

    var isMacro: Bool {
        switch self {
        case .calories, .protein, .carbs, .fat, .fiber, .sugar, .satFat: return true
        default: return false
        }
    }
    var isMicro: Bool { !isMacro }

    /// Micronutrients surfaced in the radar / highlights (the ones most relevant
    /// to recomposition & common deficiencies, esp. for vegetarians).
    static var radarKeys: [NutrientKey] {
        [.iron, .calcium, .magnesium, .potassium, .zinc, .b12, .vitD, .vitC]
    }
}

struct Nutrients: Codable, Equatable {
    private(set) var values: [NutrientKey: Double]

    init(_ values: [NutrientKey: Double] = [:]) { self.values = values }

    subscript(_ key: NutrientKey) -> Double {
        get { values[key] ?? 0 }
        set { values[key] = newValue }
    }

    // Convenience macro accessors
    var calories: Double { self[.calories] }
    var protein: Double  { self[.protein] }
    var carbs: Double    { self[.carbs] }
    var fat: Double      { self[.fat] }
    var fiber: Double    { self[.fiber] }

    static let zero = Nutrients()

    func scaled(by factor: Double) -> Nutrients {
        Nutrients(values.mapValues { $0 * factor })
    }

    static func + (lhs: Nutrients, rhs: Nutrients) -> Nutrients {
        var out = lhs.values
        for (k, v) in rhs.values { out[k, default: 0] += v }
        return Nutrients(out)
    }

    static func += (lhs: inout Nutrients, rhs: Nutrients) { lhs = lhs + rhs }

    static func sum(_ items: [Nutrients]) -> Nutrients {
        items.reduce(.zero, +)
    }

    /// Calories derived from macros (Atwater) — useful for validation/labels.
    var caloriesFromMacros: Double { protein * 4 + carbs * 4 + fat * 9 }

    // MARK: Codable (persist as [String: Double] for stability / SwiftData)
    init(from decoder: Decoder) throws {
        let raw = try decoder.singleValueContainer().decode([String: Double].self)
        var dict: [NutrientKey: Double] = [:]
        for (k, v) in raw { if let key = NutrientKey(rawValue: k) { dict[key] = v } }
        self.values = dict
    }
    func encode(to encoder: Encoder) throws {
        var c = encoder.singleValueContainer()
        try c.encode(Dictionary(uniqueKeysWithValues: values.map { ($0.key.rawValue, $0.value) }))
    }
}

/// Daily targets the user is held to (computed by TargetsEngine, editable in Settings).
struct NutritionTargets: Codable, Equatable {
    var calories: Double
    var protein: Double
    var carbs: Double
    var fat: Double
    var fiber: Double
    var steps: Int
    /// Micronutrient daily reference intakes used for %RDA bars.
    var micros: [NutrientKey: Double]

    static let placeholder = NutritionTargets(
        calories: 2100, protein: 160, carbs: 200, fat: 60, fiber: 30, steps: 10000,
        micros: [:]
    )
}
