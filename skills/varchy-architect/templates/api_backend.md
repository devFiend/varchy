# Architectural Archetype: High-Throughput API Backend

Use this template archetype when designing scalable REST or GraphQL backend services, microservices, or public developer APIs.

---

## 🏛️ Recommended Technology Stack

| Layer | Recommended Choice | Architectural Rationale |
|---|---|---|
| **Runtime / Language** | Go (Golang) or Python (FastAPI / asyncpg) | Lightweight concurrency, low memory footprint, and high request throughput. |
| **API Gateway / Proxy** | Envoy / Traefik / Cloudflare | Edge SSL termination, automated rate limiting, and request routing. |
| **Primary Datastore** | PostgreSQL / CockroachDB | ACID compliance with read replicas for horizontal scale. |
| **In-Memory Cache** | Redis Cluster | Sub-millisecond read response times and distributed locking. |
| **Message Broker** | Apache Kafka / RabbitMQ | Asynchronous event streaming and decoupled service-to-service communication. |
| **Observability** | OpenTelemetry + Prometheus + Grafana | Distributed tracing across microservice boundaries. |

---

## 🔒 Security & API Governance
* **Authentication:** OAuth2 Bearer tokens (JWT) or scoped API Keys (`varch_live_...`).
* **Rate Limiting:** Token-bucket algorithm per IP and authenticated API key.
* **Idempotency:** `Idempotency-Key` HTTP header required on all POST/PUT mutations.
* **Versioning:** URL path versioning (`/api/v1/...`).

