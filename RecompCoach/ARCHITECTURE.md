# Architecture

## 1. High-level

```
            ┌─────────────────────────────────────────────┐
            │                   SwiftUI Views               │
            │  Onboarding · Dashboard · Diary · DietBuilder │
            │  Progress · Activity · Coach · Settings       │
            └───────────────▲──────────────┬───────────────┘
                            │ @Observable    │ user intent
            ┌───────────────┴──────────────▼───────────────┐
            │                  ViewModels (MVVM)            │
            └───────────────▲──────────────┬───────────────┘
                            │               │
        ┌───────────────────┴───┐   ┌───────▼─────────────────────┐
        │   Domain Services      │   │        Repositories          │
        │  NutritionCalculator   │   │  (CRUD over SwiftData)       │
        │  TargetsEngine         │   └───────▲─────────────────────┘
        │  CoachingEngine        │           │
        │  HealthKitService      │   ┌───────┴─────────────────────┐
        │  SyncService / Outbox  │   │  Persistence (SwiftData)     │
        │  APIClient / AICoach   │   │  + Data Protection + Keychain│
        └───────────────────────┘   └──────────────────────────────┘
                            │ (online only)
                    ┌───────▼────────┐
                    │  Cloud Backend  │  REST: /sync, /foods, /coach
                    └────────────────┘
```

Everything below the ViewModels is injected through a single `AppEnvironment` (constructor injection), which makes the app testable and keeps offline/online concerns isolated in services.

## 2. Offline-first strategy
- **Single source of truth = on-device SwiftData store** (SQLite). The UI only ever reads/writes locally, so it is always responsive and fully functional offline.
- **Writes** also append a compact operation to an **Outbox** (`OutboxItem`). When connectivity returns (`NWPathMonitor`), `SyncService` flushes the outbox to the backend with last-write-wins + `updatedAt` conflict handling.
- **Reads from cloud** (multi-device) merge server records by `id`/`updatedAt`.
- **Food database**: a read-only seed (`foods.json`) is imported into SwiftData on first launch. When online, `/foods?since=` deltas are merged. Search runs locally with `#Predicate`, so it works offline.
- **HealthKit** data (steps/distance/active energy) is cached into `ActivityLog` rows so the dashboard shows activity even if Health is temporarily unavailable.

## 3. Encryption at rest
- SwiftData's store file is created with `FileProtectionType.complete` (`Info.plist` not required — set on the store URL). On a passcode-locked device the SQLite file is encrypted by iOS Data Protection.
- A symmetric `SymmetricKey` (CryptoKit) is stored in the **Keychain** (`Encryption.swift`) and used to encrypt exported backups and any field-level secrets (e.g., auth tokens) via AES-GCM.
- Production option documented for SQLCipher if regulatory full-DB encryption is required beyond Data Protection.

## 4. MVVM contract
- Views are dumb; they bind to an `@Observable` (Observation framework) view model.
- View models depend only on protocols (`FoodRepository`, `ActivityProviding`, etc.) so they can be unit-tested with fakes.
- Domain math (calories, macros, micros, coaching) lives in **pure, side-effect-free services** that are trivially testable.

## 5. Science core (deterministic, offline)
- `TargetsEngine`: Mifflin–St Jeor BMR → activity multiplier → TDEE → goal-adjusted calories; protein g/kg (lean-mass aware), fat g/kg, carbs as remainder, fiber per 1000 kcal, micronutrient RDAs by sex/age.
- `NutritionCalculator`: scale a `FoodItem` by grams, sum `Nutrients`, compute %RDA.
- `CoachingEngine`: weekly trend analysis → typed `CoachingInsight`s with rationale. Pure function of inputs → output, so it runs offline and is unit-tested.

## 6. Online enhancements (graceful degradation)
- `AICoachService` calls `/coach/chat` only when reachable; otherwise the UI shows the rules-based answer and a "connect for deeper Q&A" affordance.
- Guidance/food refresh endpoints are deltas; failures are non-fatal.

## 7. Testing
- `Tests/` contains unit tests for `TargetsEngine`, `NutritionCalculator`, and `CoachingEngine` (the parts that carry correctness risk). UI is verified via SwiftUI Previews and a smoke `XCUITest` for onboarding → log food → dashboard.
```
