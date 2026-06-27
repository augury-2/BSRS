import Foundation

enum Sex: String, Codable, CaseIterable, Identifiable {
    case male, female
    var id: String { rawValue }
    var title: String { self == .male ? "Male" : "Female" }
}

enum GoalType: String, Codable, CaseIterable, Identifiable {
    case loseFatMaintainMuscle
    case loseFatGainMuscle
    case maintain

    var id: String { rawValue }
    var title: String {
        switch self {
        case .loseFatMaintainMuscle: return "Lose fat & maintain muscle"
        case .loseFatGainMuscle:     return "Lose fat & gain muscle"
        case .maintain:              return "Maintain body composition"
        }
    }
    /// Fraction of TDEE applied as a deficit (negative) or surplus (positive).
    var calorieAdjustment: Double {
        switch self {
        case .loseFatMaintainMuscle: return -0.20   // moderate deficit
        case .loseFatGainMuscle:     return -0.12   // mild deficit → recomposition
        case .maintain:              return  0.0
        }
    }
}

enum ActivityLevel: String, Codable, CaseIterable, Identifiable {
    case sedentary, light, moderate, active, veryActive
    var id: String { rawValue }
    var title: String {
        switch self {
        case .sedentary:  return "Sedentary (desk job, little exercise)"
        case .light:      return "Lightly active (1–3 days/wk)"
        case .moderate:   return "Moderately active (3–5 days/wk)"
        case .active:     return "Active (6–7 days/wk)"
        case .veryActive: return "Very active (physical job + training)"
        }
    }
    /// Mifflin–St Jeor activity multiplier.
    var multiplier: Double {
        switch self {
        case .sedentary:  return 1.2
        case .light:      return 1.375
        case .moderate:   return 1.55
        case .active:     return 1.725
        case .veryActive: return 1.9
        }
    }
}

enum MealType: String, Codable, CaseIterable, Identifiable {
    case breakfast, lunch, dinner, snack
    var id: String { rawValue }
    var title: String { rawValue.capitalized }
    var systemImage: String {
        switch self {
        case .breakfast: return "sunrise.fill"
        case .lunch:     return "sun.max.fill"
        case .dinner:    return "moon.stars.fill"
        case .snack:     return "leaf.fill"
        }
    }
}

enum TemplateKind: String, Codable, CaseIterable, Identifiable {
    case trainingDay, restDay, cuttingDay, custom
    var id: String { rawValue }
    var title: String {
        switch self {
        case .trainingDay: return "Training Day"
        case .restDay:     return "Rest Day"
        case .cuttingDay:  return "Cutting Day"
        case .custom:      return "Custom"
        }
    }
}

enum ActivityKind: String, Codable {
    case steps        // auto from HealthKit
    case strength
    case cardio
    case other
}

enum DataSource: String, Codable {
    case healthKit, manual, seed, cloud, userCustom
}

enum Units: String, Codable, CaseIterable, Identifiable {
    case metric, imperial
    var id: String { rawValue }
    var weightUnit: String { self == .metric ? "kg" : "lb" }
    var lengthUnit: String { self == .metric ? "cm" : "in" }
}
