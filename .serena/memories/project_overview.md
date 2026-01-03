# Study Abroad Project Overview

## Purpose
Build a web application (MVP UK Study & Migration Research App) with a Gemini-style conversational interface that allows students—primarily from South Asia—to generate paid, structured research reports about studying and working in a destination country (UK only for MVP).

## Key Features
- Gemini-style conversational chat interface
- Authentication via Google, Apple, Facebook, Email (using Clerk)
- Payment per query (£2.99) via Stripe
- AI-generated research reports using Gemini APIs with streaming responses
- Report storage and retrieval for 30 days (soft delete pattern)
- Three environment modes: dev, test, production with feature flags

## Architecture
Monorepo structure with:
- **Frontend**: Next.js 15+ (App Router, TypeScript strict mode, Tailwind CSS)
- **Backend**: FastAPI (Python 3.12+) with LangChain for AI orchestration
- **Database**: Supabase PostgreSQL (with local PostgreSQL for dev mode)
- **Shared Packages**: 4 infrastructure packages (config, feature-flags, database, logging)

## Current Status
- **Gate1 (Architecture)**: PASS (6 ADRs created)
- **Gate2 (Design)**: PASS (OpenAPI spec, database schemas, UX flows complete)
- **Gate3 (Implementation)**: PENDING - Ready for implementation
- All design artifacts complete in `/Users/vihang/projects/study-abroad/docs/`

## Monorepo Structure
```
study-abroad/
├── frontend/          # Next.js App Router application
├── backend/           # FastAPI Python backend
├── shared/            # Shared TypeScript packages (config, feature-flags, database, logging)
├── docs/              # Comprehensive documentation (adr, api, database, design, flows)
├── specs/             # Feature specifications
├── .specify/          # Speckit framework
├── .claude/           # Claude Code configuration
└── agents/            # Agent definitions and quality gate checklists
```

## Key Documentation
- Specification: `/Users/vihang/projects/study-abroad/specs/001-mvp-uk-study-migration/spec.md`
- Implementation Plan: `/Users/vihang/projects/study-abroad/specs/001-mvp-uk-study-migration/plan.md`
- Constitution: `/Users/vihang/projects/study-abroad/.specify/memory/constitution.md` (v1.0.0)
- ADRs: `/Users/vihang/projects/study-abroad/docs/adr/` (6 architectural decisions documented)
