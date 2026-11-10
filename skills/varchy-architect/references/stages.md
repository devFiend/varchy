# Varchy 7-Stage Architectural Reference Guide

This document defines the strict specification requirements for each stage of the Varchy architecture generation lifecycle.

---

## 1. Product Requirements Document (PRD)
* **Destination:** `docs/01-product/prd.md`
* **Structure:**
  * **Executive Summary**: 2-3 sentence thesis of the software product.
  * **Target Personas**: Detailed user archetypes with pain points and desired outcomes.
  * **Requirements Matrix**:
    ```markdown
    | ID | Feature | Priority | Description | Acceptance Criteria |
    |---|---|:---:|---|---|
    | REQ-001 | User Onboarding | Critical | Magic link & social auth | JWT returned, session initialized |
    | REQ-002 | Billing Portal | High | Stripe subscription checkout | Webhook handling, plan tier updated |
    ```
  * **Non-Functional Requirements**: Latency (<200ms p95), Security (SOC2 compliance), Scalability (10k concurrent users).

---

## 2. Design & Screen Specifications
* **Destination:** `docs/02-design/screens.md`
* **Structure:**
  * **Screen Hierarchy**: Route mapping (e.g. `/`, `/auth/login`, `/dashboard`, `/settings/billing`).
  * **State Machine per Screen**:
    * `SCREEN-001 [Dashboard]`:
      * *Empty State*: Illustration + CTA "Create your first project".
      * *Loading State*: Skeleton shimmer covering stat cards and table.
      * *Success State*: Active metrics and table of recent projects.
      * *Error State*: Banner alert with exponential backoff retry button.

---

## 3. Engineering & Component Architecture
* **Destination:** `docs/03-engineering/architecture.md`
* **Structure:**
  * **System Architecture Diagram (Mermaid)**:
    ```mermaid
    flowchart TD
      Client[Web / Mobile Client] --> Gateway[API Gateway / Edge Router]
      Gateway --> CoreAPI[Application Service]
      CoreAPI --> Database[(PostgreSQL)]
      CoreAPI --> Cache[(Redis)]
      CoreAPI --> Queue[Event Queue]
    ```
  * **Component Breakdown**: Responsibilities and boundaries for each subsystem.
  * **Technology Stack Rationale**: Explanation of why each database, framework, and external vendor was chosen.

---

## 4. Database Schemas & API Contracts
* **Destination:** `docs/03-engineering/database.md`
* **Structure:**
  * **Entity Specifications (`ENT-xxx`)**:
    * Entity name, storage engine, fields, data types, constraints, and index strategy.
  * **API Endpoints (`API-xxx`)**:
    * Method, Path, Authentication required, Request body schema, Success response (200/201), Error responses (400/401/404/500).

---

## 5. Development Task DAG
* **Destination:** `docs/04-development/tasks.md`
* **Structure:**
  * Phased breakdown:
    * `Phase 1: Foundations`
    * `Phase 2: Data Models & Business Logic`
    * `Phase 3: Frontend & Interaction`
    * `Phase 4: Hardening & Testing`
  * Each task specification:
    ```markdown
    ### [TASK-001] Setup Multi-Tenant PostgreSQL Schema
    - **Phase:** Phase 1
    - **Priority:** Critical
    - **Dependencies:** None (Root task)
    - **Realizes Requirements:** REQ-001, REQ-002
    - **Completion Criteria:**
      - [ ] Migration creates `organizations` and `users` tables
      - [ ] Row-Level Security (RLS) policies enforced
      - [ ] Automated migration test passes
    ```

---

## 6. Testing Strategy
* **Destination:** `docs/05-quality/testing.md`
* **Structure:**
  * Unit test matrix (models, domain services, utility functions).
  * Integration tests (API endpoints with mock DB).
  * End-to-end critical path user journey tests.
