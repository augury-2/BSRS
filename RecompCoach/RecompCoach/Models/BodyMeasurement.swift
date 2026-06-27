import Foundation
import SwiftData

@Model
final class BodyMeasurement {
    @Attribute(.unique) var id: UUID
    var dayKey: String
    var date: Date
    var weightKg: Double?
    var bodyFatPercent: Double?
    var waistCm: Double?
    var hipCm: Double?
    var chestCm: Double?
    var thighCm: Double?
    var armCm: Double?
    var note: String?
    var updatedAt: Date

    init(id: UUID = UUID(),
         date: Date = .now,
         weightKg: Double? = nil,
         bodyFatPercent: Double? = nil,
         waistCm: Double? = nil,
         hipCm: Double? = nil,
         chestCm: Double? = nil,
         thighCm: Double? = nil,
         armCm: Double? = nil,
         note: String? = nil) {
        self.id = id
        self.dayKey = DayKey.string(from: date)
        self.date = date
        self.weightKg = weightKg
        self.bodyFatPercent = bodyFatPercent
        self.waistCm = waistCm
        self.hipCm = hipCm
        self.chestCm = chestCm
        self.thighCm = thighCm
        self.armCm = armCm
        self.note = note
        self.updatedAt = .now
    }
}

/// Outbox operation queued for cloud sync (offline-first).
@Model
final class OutboxItem {
    @Attribute(.unique) var id: UUID
    var entity: String      // "nutritionEntry", "bodyMeasurement", ...
    var type: String        // "upsert" | "delete"
    var payload: Data
    var recordUpdatedAt: Date
    var attempts: Int
    var createdAt: Date

    init(id: UUID = UUID(), entity: String, type: String, payload: Data, recordUpdatedAt: Date = .now) {
        self.id = id
        self.entity = entity
        self.type = type
        self.payload = payload
        self.recordUpdatedAt = recordUpdatedAt
        self.attempts = 0
        self.createdAt = .now
    }
}
