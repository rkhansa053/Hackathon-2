---
id: 001
title: Update CLAUDE.md with phase 2 requirements
stage: misc
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: bs
command: Update CLAUDE.md file
labels: [documentation, configuration, phase2, agents, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - CLAUDE.md
tests:
 - Reviewed CLAUDE.md structure and updated with phase 2 requirements
---

## Prompt

Update the claude.md file based on my project requirements. In this file:

Use Auth Agent for authentication
Use Frontend Agent for frontend development (e.g., Next.js)
Use DB Agent for database design and operations
Use Backend Agent for FastAPI development
Below are my project requirements: Phase II: Todo Full-Stack Web Application
Basic Level Functionality
Objective: Using Claude Code and Spec-Kit Plus transform the console app into a modern multi-user web application with persistent storage.
💡Development Approach: Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed. We will review the process, prompts, and iterations to judge each phase and project.
Requirements
Implement all 5 Basic Level features as a web application
Create RESTful API endpoints
Build responsive frontend interface
Store data in Neon Serverless PostgreSQL database
Authentication – Implement user signup/signin using Better Auth
Technology Stack
Layer
Technology
Frontend
Next.js 16+ (App Router)
Backend
Python FastAPI
ORM
SQLModel
Database
Neon Serverless PostgreSQL
Spec-Driven
Claude Code + Spec-Kit Plus
Authentication
Better Auth.

Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.
How It Works
User logs in on Frontend → Better Auth creates a session and issues a JWT token
Frontend makes API call → Includes the JWT token in the Authorization: Bearer <token> header
Backend receives request → Extracts token from header, verifies signature using shared secret
Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
Backend filters data → Returns only tasks belonging to that user

## Response snapshot

Updated CLAUDE.md with project-specific agent usage guidelines:
- Added "Project-Specific Agent Usage" section at the top of the file
- Documented the technology stack: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT
- Specified when to use each specialized agent:
  - auth-security-agent: Authentication, JWT management, Better Auth integration
  - nextjs-frontend-agent: Frontend UI, responsive layouts, App Router patterns
  - neon-postgres-agent: Database schema design, migrations, SQLModel queries
  - fastapi-api-auth-db: REST API endpoints, Pydantic validation, async operations
- Documented the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- Retained all original Claude Code Rules content while adding project-specific context

## Outcome

- ✅ Impact: Updated project configuration to clearly specify which agents to use for different aspects of the full-stack Todo application
- 🧪 Tests: Reviewed current CLAUDE.md structure and successfully applied updates
- 📁 Files: Modified CLAUDE.md to include Phase 2 project requirements and agent usage guidelines
- 🔁 Next prompts: Create feature specifications for each of the 5 Basic Level features
- 🧠 Reflection: The agent-specific guidelines will help ensure consistent and appropriate agent selection throughout the project development.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate that agent selection is followed in subsequent development prompts
