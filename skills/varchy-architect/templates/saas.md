# Architectural Archetype: B2B Multi-Tenant SaaS

Use this template archetype when designing web-based SaaS platforms with organizations, subscriptions, and role-based permissions.

---

## 🏛️ Recommended Technology Stack

| Layer | Recommended Choice | Architectural Rationale |
|---|---|---|
| **Frontend** | Next.js (App Router) + Tailwind CSS + shadcn/ui | Server components for speed, SEO, and fast developer velocity. |
| **Backend API** | Node.js (TypeScript) / Python FastAPI | Type-safe request validation and high asynchronous throughput. |
| **Primary Database** | PostgreSQL + Prisma / Drizzle ORM | Robust relational integrity and Row-Level Security (RLS) for tenant isolation. |
| **Cache & Queues** | Redis + BullMQ | Session caching, API rate limiting, and background worker queues. |
| **Authentication** | Supabase Auth / Clerk / NextAuth | Turnkey multi-factor auth, social logins, and organization management. |
| **Billing & Payments** | Stripe Billing & Webhooks | Subscription tiers, customer portal, and proration handling. |
| **Object Storage** | Cloudflare R2 / AWS S3 | S3-compatible storage with zero egress fees. |

---

## 🔒 Security & Multi-Tenancy Model
* **Tenant Isolation:** Enforce tenant separation using either:
  1. Shared database with `organization_id` on all tables guarded by PostgreSQL Row-Level Security (RLS).
  2. Schema-per-tenant for enterprise isolation tiers.
* **RBAC Roles:** `Owner`, `Admin`, `Member`, `Billing Manager`.

---

## 📋 Core Architectural Entities

```markdown
- Organization (id, name, slug, stripe_customer_id, plan_tier, created_at)
- User (id, email, full_name, avatar_url, created_at)
- Membership (id, organization_id, user_id, role, created_at)
- Subscription (id, organization_id, stripe_subscription_id, status, current_period_end)
- AuditLog (id, organization_id, actor_id, action, resource, metadata, timestamp)
```

