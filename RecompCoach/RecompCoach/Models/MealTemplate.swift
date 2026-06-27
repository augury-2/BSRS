import Foundation
import SwiftData

struct TemplateItem: Codable, Identifiable, Equatable {
    var id: UUID = UUID()
    var foodID: UUID
    var foodName: String
    var grams: Double
}

/// A saved diet (e.g. "Cutting Day", "Training Day") the user can apply to any
/// future day with one tap.
@Model
final class MealTemplate {
    @Attribute(.unique) var id: UUID
    var name: String
    var kindRaw: String
    var itemsData: Data         // encoded [TemplateItem]
    var createdAt: Date
    var updatedAt: Date

    init(id: UUID = UUID(),
         name: String,
         kind: TemplateKind = .custom,
         items: [TemplateItem] = []) {
        self.id = id
        self.name = name
        self.kindRaw = kind.rawValue
        self.itemsData = (try? JSONEncoder().encode(items)) ?? Data()
        self.createdAt = .now
        self.updatedAt = .now
    }

    var kind: TemplateKind { get { TemplateKind(rawValue: kindRaw) ?? .custom } set { kindRaw = newValue.rawValue } }

    var items: [TemplateItem] {
        get { (try? JSONDecoder().decode([TemplateItem].self, from: itemsData)) ?? [] }
        set { itemsData = (try? JSONEncoder().encode(newValue)) ?? Data(); updatedAt = .now }
    }
}
