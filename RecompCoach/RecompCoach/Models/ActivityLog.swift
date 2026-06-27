import Foundation
import SwiftData

/// One activity record per day for auto steps (HealthKit) plus zero-or-more
/// manual workouts. Steps/distance are cached so the dashboard works offline.
@Model
final class ActivityLog {
    @Attribute(.unique) var id: UUID
    var dayKey: String
    var date: Date
    var kindRaw: String
    var name: String
    var sourceRaw: String
    var steps: Int?
    var distanceMeters: Double?
    var activeMinutes: Int?
    var durationMinutes: Double?
    var energyKcal: Double
    var updatedAt: Date

    init(id: UUID = UUID(),
         date: Date = .now,
         kind: ActivityKind,
         name: String,
         source: DataSource,
         steps: Int? = nil,
         distanceMeters: Double? = nil,
         activeMinutes: Int? = nil,
         durationMinutes: Double? = nil,
         energyKcal: Double = 0) {
        self.id = id
        self.dayKey = DayKey.string(from: date)
        self.date = date
        self.kindRaw = kind.rawValue
        self.name = name
        self.sourceRaw = source.rawValue
        self.steps = steps
        self.distanceMeters = distanceMeters
        self.activeMinutes = activeMinutes
        self.durationMinutes = durationMinutes
        self.energyKcal = energyKcal
        self.updatedAt = .now
    }

    var kind: ActivityKind { ActivityKind(rawValue: kindRaw) ?? .other }
    var source: DataSource { DataSource(rawValue: sourceRaw) ?? .manual }
}
