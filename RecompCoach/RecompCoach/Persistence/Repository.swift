import Foundation
import SwiftData

/// Abstraction over local persistence so view models stay testable.
/// The production implementation is `SwiftDataStore`; tests use an in-memory fake.
@MainActor
protocol AppStore: AnyObject {
    // Profile
    func currentProfile() -> UserProfile?
    func saveProfile(_ profile: UserProfile)

    // Foods
    func searchFoods(_ query: String, limit: Int) -> [FoodItem]
    func food(by id: UUID) -> FoodItem?
    func recentFoods(limit: Int) -> [FoodItem]
    @discardableResult func upsertCustomFood(name: String, servingGrams: Double, per100g: Nutrients) -> FoodItem

    // Diary
    func entries(on date: Date) -> [NutritionEntry]
    func entries(in range: ClosedRange<Date>) -> [NutritionEntry]
    func addEntry(food: FoodItem, grams: Double, meal: MealType, date: Date)
    func addRawEntry(_ entry: NutritionEntry)
    func deleteEntry(_ entry: NutritionEntry)

    // Templates
    func templates() -> [MealTemplate]
    func saveTemplate(_ template: MealTemplate)
    func deleteTemplate(_ template: MealTemplate)
    func applyTemplate(_ template: MealTemplate, to date: Date, meal: MealType)

    // Activity
    func activity(on date: Date) -> [ActivityLog]
    func activity(in range: ClosedRange<Date>) -> [ActivityLog]
    func upsertSteps(_ steps: Int, distanceMeters: Double?, activeMinutes: Int?, activeEnergy: Double?, on date: Date)
    func addWorkout(_ log: ActivityLog)

    // Measurements
    func measurements() -> [BodyMeasurement]
    func addMeasurement(_ m: BodyMeasurement)
    func deleteMeasurement(_ m: BodyMeasurement)

    // Sync outbox
    func enqueue(entity: String, type: String, payload: Data, updatedAt: Date)
    func pendingOutbox() -> [OutboxItem]
    func removeOutbox(_ item: OutboxItem)
}

@MainActor
final class SwiftDataStore: AppStore {
    let context: ModelContext
    init(context: ModelContext) { self.context = context }

    private func save() { try? context.save() }

    // MARK: Profile
    func currentProfile() -> UserProfile? {
        try? context.fetch(FetchDescriptor<UserProfile>()).first
    }
    func saveProfile(_ profile: UserProfile) {
        if currentProfile()?.id != profile.id { context.insert(profile) }
        profile.updatedAt = .now
        save()
        enqueueCodable(entity: "profile", type: "upsert", value: ProfileDTO(profile))
    }

    // MARK: Foods
    func searchFoods(_ query: String, limit: Int = 40) -> [FoodItem] {
        let q = query.trimmingCharacters(in: .whitespaces)
        var descriptor = FetchDescriptor<FoodItem>(sortBy: [SortDescriptor(\.name)])
        if !q.isEmpty {
            descriptor.predicate = #Predicate { $0.name.localizedStandardContains(q) }
        }
        descriptor.fetchLimit = limit
        return (try? context.fetch(descriptor)) ?? []
    }
    func food(by id: UUID) -> FoodItem? {
        var d = FetchDescriptor<FoodItem>(predicate: #Predicate { $0.id == id })
        d.fetchLimit = 1
        return try? context.fetch(d).first ?? nil
    }
    func recentFoods(limit: Int = 12) -> [FoodItem] {
        // Derive from recent diary entries, de-duplicated by foodID.
        var d = FetchDescriptor<NutritionEntry>(sortBy: [SortDescriptor(\.loggedAt, order: .reverse)])
        d.fetchLimit = 60
        let recent = (try? context.fetch(d)) ?? []
        var seen = Set<UUID>(); var result: [FoodItem] = []
        for e in recent {
            guard let fid = e.foodID, !seen.contains(fid), let f = food(by: fid) else { continue }
            seen.insert(fid); result.append(f)
            if result.count >= limit { break }
        }
        return result
    }
    @discardableResult
    func upsertCustomFood(name: String, servingGrams: Double, per100g: Nutrients) -> FoodItem {
        let f = FoodItem(name: name, servingDescription: "1 serving (\(Int(servingGrams)) g)",
                         defaultServingGrams: servingGrams, per100g: per100g,
                         isCustom: true, source: .userCustom)
        context.insert(f); save()
        enqueueCodable(entity: "food", type: "upsert", value: FoodDTO(f))
        return f
    }

    // MARK: Diary
    func entries(on date: Date) -> [NutritionEntry] {
        let key = DayKey.string(from: date)
        let d = FetchDescriptor<NutritionEntry>(
            predicate: #Predicate { $0.dayKey == key },
            sortBy: [SortDescriptor(\.loggedAt)])
        return (try? context.fetch(d)) ?? []
    }
    func entries(in range: ClosedRange<Date>) -> [NutritionEntry] {
        let lo = range.lowerBound, hi = range.upperBound
        let d = FetchDescriptor<NutritionEntry>(
            predicate: #Predicate { $0.loggedAt >= lo && $0.loggedAt <= hi },
            sortBy: [SortDescriptor(\.loggedAt)])
        return (try? context.fetch(d)) ?? []
    }
    func addEntry(food: FoodItem, grams: Double, meal: MealType, date: Date) {
        let entry = NutritionEntry(date: date, meal: meal, foodID: food.id,
                                   foodName: food.name, quantityGrams: grams,
                                   nutrients: food.nutrients(forGrams: grams))
        addRawEntry(entry)
    }
    func addRawEntry(_ entry: NutritionEntry) {
        context.insert(entry); save()
        enqueueCodable(entity: "nutritionEntry", type: "upsert", value: EntryDTO(entry))
    }
    func deleteEntry(_ entry: NutritionEntry) {
        let id = entry.id
        context.delete(entry); save()
        enqueue(entity: "nutritionEntry", type: "delete", payload: idPayload(id), updatedAt: .now)
    }

    // MARK: Templates
    func templates() -> [MealTemplate] {
        (try? context.fetch(FetchDescriptor<MealTemplate>(sortBy: [SortDescriptor(\.name)]))) ?? []
    }
    func saveTemplate(_ template: MealTemplate) {
        if !templates().contains(where: { $0.id == template.id }) { context.insert(template) }
        template.updatedAt = .now; save()
    }
    func deleteTemplate(_ template: MealTemplate) { context.delete(template); save() }
    func applyTemplate(_ template: MealTemplate, to date: Date, meal: MealType) {
        for item in template.items {
            guard let food = food(by: item.foodID) else { continue }
            addEntry(food: food, grams: item.grams, meal: meal, date: date)
        }
    }

    // MARK: Activity
    func activity(on date: Date) -> [ActivityLog] {
        let key = DayKey.string(from: date)
        let d = FetchDescriptor<ActivityLog>(predicate: #Predicate { $0.dayKey == key })
        return (try? context.fetch(d)) ?? []
    }
    func activity(in range: ClosedRange<Date>) -> [ActivityLog] {
        let lo = range.lowerBound, hi = range.upperBound
        let d = FetchDescriptor<ActivityLog>(
            predicate: #Predicate { $0.date >= lo && $0.date <= hi },
            sortBy: [SortDescriptor(\.date)])
        return (try? context.fetch(d)) ?? []
    }
    func upsertSteps(_ steps: Int, distanceMeters: Double?, activeMinutes: Int?, activeEnergy: Double?, on date: Date) {
        let existing = activity(on: date).first { $0.kind == .steps }
        if let log = existing {
            log.steps = steps
            log.distanceMeters = distanceMeters
            log.activeMinutes = activeMinutes
            if let e = activeEnergy { log.energyKcal = e }
            log.updatedAt = .now
        } else {
            let log = ActivityLog(date: date, kind: .steps, name: "Steps", source: .healthKit,
                                  steps: steps, distanceMeters: distanceMeters,
                                  activeMinutes: activeMinutes, energyKcal: activeEnergy ?? 0)
            context.insert(log)
        }
        save()
    }
    func addWorkout(_ log: ActivityLog) { context.insert(log); save() }

    // MARK: Measurements
    func measurements() -> [BodyMeasurement] {
        (try? context.fetch(FetchDescriptor<BodyMeasurement>(sortBy: [SortDescriptor(\.date)]))) ?? []
    }
    func addMeasurement(_ m: BodyMeasurement) {
        context.insert(m); save()
        enqueueCodable(entity: "bodyMeasurement", type: "upsert", value: MeasurementDTO(m))
    }
    func deleteMeasurement(_ m: BodyMeasurement) { context.delete(m); save() }

    // MARK: Outbox
    func enqueue(entity: String, type: String, payload: Data, updatedAt: Date) {
        context.insert(OutboxItem(entity: entity, type: type, payload: payload, recordUpdatedAt: updatedAt))
        save()
    }
    func pendingOutbox() -> [OutboxItem] {
        (try? context.fetch(FetchDescriptor<OutboxItem>(sortBy: [SortDescriptor(\.createdAt)]))) ?? []
    }
    func removeOutbox(_ item: OutboxItem) { context.delete(item); save() }

    // MARK: Helpers
    private func idPayload(_ id: UUID) -> Data { (try? JSONEncoder().encode(["id": id.uuidString])) ?? Data() }
    private func enqueueCodable<T: Encodable>(entity: String, type: String, value: T) {
        guard let data = try? JSONEncoder().encode(value) else { return }
        enqueue(entity: entity, type: type, payload: data, updatedAt: .now)
    }
}
