import Foundation
import Network
import Observation

/// Lightweight connectivity monitor. Drives offline/online UI affordances and
/// triggers the sync outbox flush when the network returns.
@Observable
final class Reachability {
    private(set) var isOnline: Bool = true
    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue(label: "app.recompcoach.reachability")
    var onBecameOnline: (() -> Void)?

    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            let online = path.status == .satisfied
            DispatchQueue.main.async {
                let was = self?.isOnline ?? true
                self?.isOnline = online
                if online && !was { self?.onBecameOnline?() }
            }
        }
        monitor.start(queue: queue)
    }

    deinit { monitor.cancel() }
}
