import SwiftUI

/// Routes to onboarding until a profile exists, then shows the main tab bar.
struct RootView: View {
    @Environment(AppEnvironment.self) private var env
    @State private var hasProfile: Bool = false
    @State private var checked = false

    var body: some View {
        Group {
            if !checked {
                ProgressView().task { refresh() }
            } else if hasProfile {
                MainTabView()
            } else {
                OnboardingFlow(onComplete: { refresh() })
            }
        }
    }

    private func refresh() {
        hasProfile = env.store.currentProfile() != nil
        checked = true
    }
}

struct MainTabView: View {
    @Environment(AppEnvironment.self) private var env

    var body: some View {
        TabView {
            DashboardView()
                .tabItem { Label("Today", systemImage: "house.fill") }
            FoodDiaryView()
                .tabItem { Label("Diary", systemImage: "fork.knife") }
            DietBuilderView()
                .tabItem { Label("Build", systemImage: "slider.horizontal.3") }
            ProgressDashboardView()
                .tabItem { Label("Progress", systemImage: "chart.xyaxis.line") }
            SettingsView()
                .tabItem { Label("Settings", systemImage: "gearshape.fill") }
        }
        .task {
            if env.store.currentProfile()?.healthSyncEnabled == true {
                try? await env.activity.requestAuthorization()
            }
        }
    }
}

#Preview {
    RootView().environment(AppEnvironment.preview())
}
