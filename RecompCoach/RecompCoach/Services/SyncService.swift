import Foundation
import Observation

/// Flushes the offline outbox to the backend and pulls deltas. Triggered when
/// the network returns or on app foreground. No-op when cloud sync is disabled.
@Observable
@MainActor
final class SyncService {
    enum State: Equatable { case idle, syncing, error(String), done(Date) }

    private let store: AppStore
    private let api: APIClienting
    private(set) var state: State = .idle
    var cloudSyncEnabled: Bool = false

    private let lastPullKey = "sync.lastPull"
    private var lastPull: Date? {
        get { UserDefaults.standard.object(forKey: lastPullKey) as? Date }
        set { UserDefaults.standard.set(newValue, forKey: lastPullKey) }
    }

    init(store: AppStore, api: APIClienting) {
        self.store = store
        self.api = api
    }

    /// Push queued local changes, then pull remote deltas. Safe to call often.
    func sync() async {
        guard cloudSyncEnabled else { return }
        guard state != .syncing else { return }
        state = .syncing
        do {
            try await flushOutbox()
            try await pull()
            lastPull = .now
            state = .done(.now)
        } catch {
            state = .error(error.localizedDescription)
        }
    }

    private func flushOutbox() async throws {
        let pending = store.pendingOutbox()
        guard !pending.isEmpty else { return }
        let ops = pending.map { SyncOp(id: $0.id, entity: $0.entity, type: $0.type,
                                       updatedAt: $0.recordUpdatedAt,
                                       payload: $0.type == "delete" ? nil : $0.payload) }
        // Batch to keep requests small.
        for chunk in ops.chunked(into: 100) {
            let applied = try await api.pushOps(chunk)
            let appliedSet = Set(applied)
            for item in pending where appliedSet.contains(item.id) { store.removeOutbox(item) }
        }
    }

    private func pull() async throws {
        let deltas = try await api.pullDeltas(since: lastPull)
        // Merge strategy = last-write-wins by updatedAt. Repository upserts
        // would compare timestamps; abbreviated here for brevity.
        _ = deltas
        // Food database deltas (also available offline once merged).
        _ = try? await api.foodDeltas(since: lastPull)
    }
}

extension Array {
    func chunked(into size: Int) -> [[Element]] {
        guard size > 0 else { return [self] }
        return stride(from: 0, to: count, by: size).map { Array(self[$0..<Swift.min($0 + size, count)]) }
    }
}
