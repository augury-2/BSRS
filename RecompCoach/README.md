# RecompCoach — Body Recomposition Coach (iOS)

A native **SwiftUI** iPhone app for **body recomposition** (lose fat, build/maintain muscle). It is an intelligent, science-backed alternative to MyFitnessPal, **offline-first** with optional cloud sync and an online AI coach.

- **Target:** iPhone 15, iOS 17+
- **Language/UI:** Swift 5.9 / SwiftUI
- **Persistence:** SwiftData (SQLite-backed) with iOS Data Protection (encryption at rest) + Keychain
- **Charts:** Swift Charts
- **Activity:** HealthKit (steps, distance, active energy)
- **Architecture:** MVVM + Repository, dependency-injected `AppEnvironment`

---

## Why this app is different
It optimizes for **recomposition**, not just weight loss:
- Protein target driven by **g/kg bodyweight** (and lean mass when body-fat % is known).
- A **rules-based coaching engine** reads your weekly trends (weight, waist, intake, steps) and tells you *what to change* — backed by mainstream sports-nutrition guidelines (ISSN, ACSM, Helms, Schoenfeld), not fads.
- A **Build My Diet** screen that recalculates full macros **and micronutrients** live as you tune portions, with a micronutrient radar and "high in / low in" highlights.

---

## Build & run

This project ships as source + an [XcodeGen](https://github.com/yonpols/XcodeGen) spec so the `.xcodeproj` can be regenerated deterministically.

```bash
# 1. Install XcodeGen (one time)
brew install xcodegen

# 2. From RecompCoach/ generate the Xcode project
cd RecompCoach
xcodegen generate

# 3. Open and run on an iPhone 15 simulator (iOS 17+)
open RecompCoach.xcodeproj
```

> No XcodeGen? Create a new **iOS App** target in Xcode (SwiftUI, iOS 17), drag the `RecompCoach/` source folders in, add the `Resources/foods.json`, and paste the keys from `Support/Info.plist` (HealthKit usage strings + background modes).

### Capabilities to enable in Xcode
- **HealthKit** (Signing & Capabilities → + HealthKit)
- **Background Modes** → *Background fetch* (for sync) — optional
- App Group / iCloud only if you extend sync to CloudKit.

---

## Project layout

```
RecompCoach/
├── project.yml                 # XcodeGen spec
├── README.md  ARCHITECTURE.md
├── Backend/API.md              # REST contract for cloud sync + AI coach
└── RecompCoach/
    ├── App/                    # App entry, environment, root tab/router
    ├── Models/                 # SwiftData @Model + value types
    ├── Persistence/            # ModelContainer, encryption, food seeding, repos
    ├── Services/               # Calculator, Targets, Coaching, HealthKit, Sync, API, AI
    ├── ViewModels/             # MVVM view models
    ├── Views/                  # SwiftUI screens + reusable components
    ├── Resources/              # foods.json seed database
    └── Support/                # Info.plist, extensions, theme
```

See **ARCHITECTURE.md** for the full design and **Backend/API.md** for the sync/AI contract.

## Status / honesty note
This is an implementation-ready reference codebase covering all requested features with real, idiomatic Swift. It was authored outside Xcode; before shipping, open it in Xcode 15, resolve any SDK-version nits, wire the HealthKit entitlement, and run the unit tests in `Tests/`.
