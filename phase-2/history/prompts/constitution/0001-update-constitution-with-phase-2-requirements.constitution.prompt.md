---
id: 0001
title: Update constitution with phase 2 requirements
stage: constitution
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: bs
command: /sp.constitution
labels: [documentation, governance, constitution, phase2, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:

## Prompt

/sp.constitution

Project: Phase II – Todo Full-Stack Web Application (Spec-Driven, Agentic Development)

Core principles:
- Spec-driven development (all implementation must trace back to specs)
- Security-first architecture (authentication, authorization, data isolation)
- Correctness over speed (no undocumented behavior)
- Deterministic, reviewable agent output (no manual coding)

Key standards:
- All features must map directly to project requirements
- All API behavior must be explicitly defined before implementation
- Authentication must be enforced on every protected endpoint
- User data isolation must be guaranteed at all layers
- JWT-based auth must be verifiable independently by backend
- No hardcoded secrets; environment variables required
- Frontend, backend, and auth flows must be consistent and compatible

Constraints:
- Development workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- Manual coding: Not allowed
- Technology stack:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth (JWT-based)
- API style: RESTful
- Auth requirement:
  - All API endpoints require valid JWT after authentication is enabled
  - Unauthorized requests must return HTTP 401

Success criteria:
- All 5 basic-level features implemented as a web application
- All REST API endpoints function correctly and securely
- Users can sign up, sign in, and manage only their own tasks
- JWT tokens are issued, transmitted, and verified correctly
- Backend enforces task ownership on every operation
- Frontend is responsive and functional across devices
- Entire system passes functional, security, and isolation review

## Response snapshot

Updated .specify/memory/constitution.md with Phase II project requirements:

Core Principles (4):
1. Spec-Driven Development - All code must trace to specs
2. Security-First Architecture - Auth required on all endpoints
3. Correctness Over Speed - No undocumented behavior
4. Deterministic Agent Output - No manual coding allowed

Technology Standards:
- Frontend: Next.js 16+, Backend: FastAPI, DB: Neon PostgreSQL
- Auth: Better Auth with JWT
- All endpoints require JWT, return 401 for unauthorized

Development Constraints:
- Workflow: Spec → Plan → Tasks → Implement
- Stack is mandatory, no substitutions
- Testing required before implementation

Success Criteria (7):
- 5 basic features as web app
- Secure REST endpoints
- JWT auth working
- User data isolation
- Responsive frontend
- System passes review

Governance:
- Version 1.0.0, ratified 2026-01-24
- All PRs must verify compliance
- Amendments require team approval

## Outcome

- ✅ Impact: Established mandatory project governance for Phase II Todo application
- 🧪 Tests: No tests required for documentation
- 📁 Files: Modified .specify/memory/constitution.md (complete rewrite)
- 🔁 Next prompts: Implement /sp.specify for todo features
- 🧠 Reflection: Constitution now enforces spec-driven, agentic development with security-first approach

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify constitution compliance during first implementation task
