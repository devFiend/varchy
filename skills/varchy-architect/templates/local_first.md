# Architectural Archetype: Local-First & Offline Sync

Use this template archetype when designing desktop, mobile, or web applications that work 100% offline and sync seamlessly to the cloud.

---

## 🏛️ Recommended Technology Stack

| Layer | Recommended Choice | Architectural Rationale |
|---|---|---|
| **Client Storage** | SQLite (via wa-sqlite / OPFS on Web, native SQLite on Desktop/Mobile) | Full SQL querying locally with zero network latency. |
| **Sync Protocol** | ElectricSQL / PowerSync / CRDTs | Incremental bi-directional change sync with conflict resolution. |
| **State Management** | Zustand / TanStack Query | Reactive local UI rendering with optimistic updates. |
| **Cloud Central DB** | PostgreSQL | Source of truth and multi-device coordination hub. |
| **Auth & Security** | Local cryptographic keystore + JWT sync tokens | Offline authentication with token refresh upon network reconnection. |

---

## 🔒 Offline Consistency Model
* **Optimistic Local Mutations:** All writes write directly to the local SQLite database instantly with zero UI waiting.
* **Sync Engine Queue:** Changes are recorded in a local `sync_mutations` outbox.
* **Conflict Resolution:** Last-Write-Wins (LWW) with logical timestamps or Conflict-Free Replicated Data Types (CRDTs).
