import Foundation
import SwiftData
import Observation

/// Single composition root. Holds services and the store, injected into the
/// view hierarchy via `.environment(...)`. Makes offline/online concerns and
/// dependencies explicit and swappable for tests/previews.
@Observable
@MainActor
final class AppEnvironment {
    let container: ModelContainer
    let store: AppStore
    let activity: ActivityProviding
    let reachability: Reachability
    let api: APIClienting
    let sync: SyncService
    let coach: AICoachService

    init(container: ModelContainer,
         activity: ActivityProviding,
         api: APIClienting = APIClient()) {
        self.container = container
        let store = SwiftDataStore(context: container.mainContext)
        self.store = store
        self.activity = activity
        let reach = Reachability()
        self.reachability = reach
        self.api = api
        let sync = SyncService(store: store, api: api)
        self.sync = sync
        self.coach = AICoachService(api: api, reachability: reach)

        // Seed the food DB on first launch (offline-ready search).
        FoodDatabaseSeeder.seedIfNeeded(context: container.mainContext)

        // Flush the outbox whenever connectivity returns.
        reach.onBecameOnline = { [weak sync] in Task { await sync?.sync() } }
    }

    /// Convenience factory for the live app.
    static func live() -> AppEnvironment {
        let container = AppDatabase.makeContainer()
        #if canImport(HealthKit)
        let provider: ActivityProviding = HealthKitService()
        #else
        let provider: ActivityProviding = MockActivityProvider()
        #endif
        return AppEnvironment(container: container, activity: provider)
    }

    /// In-memory environment for SwiftUI previews & tests.
    static func preview() -> AppEnvironment {
        let container = AppDatabase.makeContainer(inMemory: true)
        let env = AppEnvironment(container: container, activity: MockActivityProvider())
        PreviewSeed.populate(env.store)
        return env
    }
}
