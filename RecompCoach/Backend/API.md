# Backend REST Contract (cloud sync + AI coach)

Base URL: `https://api.recompcoach.app/v1`
Auth: `Authorization: Bearer <jwt>` (obtained from `/auth`). All bodies are JSON.
All sync is **optional** — the app is fully functional without ever calling these.

## Auth
```
POST /auth/apple          # Sign in with Apple → { token, userId }
POST /auth/refresh        # { refreshToken } → { token }
DELETE /account           # delete-account (GDPR) → 204
GET  /account/export      # → application/json full data export
```

## Sync (outbox flush + pull)
The client maintains an **outbox** of operations. It flushes them, then pulls deltas.

```
POST /sync/push
  Body: { ops: [SyncOp] }            # idempotent by op.id
  → { applied: [opId], serverTime }

GET  /sync/pull?since=<ISO8601>
  → { profile?, foods:[], entries:[], templates:[], activity:[], measurements:[], serverTime }
```

`SyncOp`:
```json
{
  "id": "uuid",                 // client-generated, idempotency key
  "entity": "nutritionEntry",   // profile|food|nutritionEntry|mealTemplate|activityLog|bodyMeasurement
  "type": "upsert",             // upsert|delete
  "updatedAt": "2026-06-27T10:00:00Z",
  "payload": { ... }            // entity JSON (omitted for delete)
}
```
Conflict resolution: **last-write-wins by `updatedAt`** per record id.

## Food database deltas
```
GET /foods?since=<ISO8601>&locale=en-IN
  → { foods: [FoodItem], serverTime }   # additions/updates since timestamp
```

## Scientific guidance refresh
```
GET /guidance?since=<ISO8601>
  → { rules: [...], rdaTables: {...}, version }   # lets coaching update without app release
```

## AI coach (online only)
```
POST /coach/chat
  Body: { messages:[{role,content}], context: WeeklySnapshot }
  → { reply, citations?: [..] }     # streamed via SSE optionally
```
`WeeklySnapshot` is the same struct `CoachingEngine` consumes, so the LLM gets identical context and can elaborate on the offline rules-based insights.

## Privacy
- Only synced if the user enables "Cloud Sync" in Settings.
- HealthKit data is never uploaded unless the user opts in to "Sync activity".
- TLS 1.2+, tokens in Keychain, at-rest encryption on device via Data Protection.
