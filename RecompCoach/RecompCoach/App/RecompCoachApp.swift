import SwiftUI
import SwiftData

@main
struct RecompCoachApp: App {
    @State private var env = AppEnvironment.live()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(env)
                .modelContainer(env.container)
                .tint(Theme.accent)
        }
    }
}
