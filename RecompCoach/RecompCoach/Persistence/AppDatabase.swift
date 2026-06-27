import Foundation
import SwiftData

/// Builds the SwiftData container for all models and applies file-level
/// encryption (Data Protection) to the underlying SQLite store.
enum AppDatabase {

    static let schema = Schema([
        UserProfile.self,
        FoodItem.self,
        NutritionEntry.self,
        MealTemplate.self,
        ActivityLog.self,
        BodyMeasurement.self,
        OutboxItem.self
    ])

    static func makeContainer(inMemory: Bool = false) -> ModelContainer {
        let config: ModelConfiguration
        if inMemory {
            config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
        } else {
            let url = URL.applicationSupportDirectory.appending(path: "RecompCoach.store")
            config = ModelConfiguration(schema: schema, url: url)
        }

        do {
            let container = try ModelContainer(for: schema, configurations: [config])
            if !inMemory { applyCompleteProtection(at: config.url) }
            return container
        } catch {
            // A corrupt store should never crash the user out permanently; in
            // production we'd surface a recovery flow. Fall back to in-memory.
            assertionFailure("Failed to create ModelContainer: \(error)")
            let fallback = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
            return try! ModelContainer(for: schema, configurations: [fallback])
        }
    }

    /// Encrypt the store file at rest. On a passcode-locked device the file is
    /// inaccessible (and encrypted) until first unlock.
    private static func applyCompleteProtection(at url: URL) {
        guard FileManager.default.fileExists(atPath: url.path) else { return }
        try? FileManager.default.setAttributes(
            [.protectionKey: FileProtectionType.completeUntilFirstUserAuthentication],
            ofItemAtPath: url.path
        )
    }
}
