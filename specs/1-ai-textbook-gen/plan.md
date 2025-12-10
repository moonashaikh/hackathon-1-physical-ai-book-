# Implementation Plan: AI-Native Textbook Generation

**Branch**: `1-ai-textbook-gen` | **Date**: 2025-12-05 | **Spec**: specs/1-ai-textbook-gen/spec.md
**Input**: Feature specification from `/specs/1-ai-textbook-gen/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation for generating a short, professional AI-native textbook with a modern Docusaurus UI and a free-tier compatible RAG chatbot. The core technical approach involves setting up Docusaurus for content presentation and integrating a FastAPI backend for the RAG chatbot, utilizing Qdrant for vector storage and Neon Postgres for metadata, all while adhering to free-tier constraints and optimizing for speed and minimalism.

## Technical Context

**Language/Version**: Python 3.11+ (for FastAPI), Node.js (for Docusaurus)
**Primary Dependencies**: Docusaurus, FastAPI, Qdrant, Neon Postgres, lightweight embedding library (e.g., Sentence Transformers with a small model)
**Storage**: Qdrant (vector embeddings), Neon Postgres (metadata)
**Testing**: Pytest (backend), Docusaurus testing utilities (frontend)
**Target Platform**: Web (Static site hosted on GitHub Pages, FastAPI backend deployed to a free-tier cloud service like Vercel/Render/Fly.io/Heroku-free-tier replacement)
**Project Type**: Web application (frontend Docusaurus, backend FastAPI)
**Performance Goals**: Textbook content loads in <2s, RAG chatbot responses in <3s, Docusaurus build in <5mins.
**Constraints**: Free API usage only, lightweight embeddings, fast/minimal build, no heavy GPU requirements.
**Scale/Scope**: Single textbook, ~6 chapters, supporting a single chatbot instance with book-specific knowledge.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- All outputs strictly follow the user intent.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.
- Record every user input verbatim in a Prompt History Record (PHR).
- Prefer CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.
- Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-textbook-gen/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/             # Pydantic models for data (e.g., Chapter, Question, Answer)
│   ├── services/           # Business logic (e.g., Qdrant/Neon interaction, embedding generation)
│   └── api/                # FastAPI endpoints
└── tests/

frontend/
├── docs/                   # Markdown files for Docusaurus chapters
├── blog/                   # Docusaurus blog (optional, remove if not used)
├── src/
│   ├── components/         # React components (e.g., Chatbot UI, Personalization button)
│   ├── pages/              # Docusaurus custom pages
│   └── theme/              # Docusaurus theme overrides and customizations
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Docusaurus sidebar configuration
└── package.json            # Frontend dependencies

.github/workflows/          # GitHub Actions for CI/CD
├── deploy-docusaurus.yml
└── deploy-fastapi.yml

.env                        # Environment variables
.gitignore
```

**Structure Decision**: The project will adopt a `backend/` and `frontend/` split. The `frontend/` directory will house the Docusaurus application, including `docs/` for chapter content and `src/` for UI components and theme customizations. The `backend/` will contain the FastAPI application for the RAG chatbot logic, with separate modules for models, services, and API endpoints. GitHub Actions will be used for CI/CD.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
## Phase 0: Research

**Objective**: Resolve all NEEDS CLARIFICATION items from Technical Context and document technology decisions.

No unresolved items - all technical context is well-defined. Research document will capture best practices and integration patterns.

## Phase 1: Design

**Objective**: Generate data model, API contracts, and quickstart guide based on research findings.

### Data Model (data-model.md)
- Entities: Chapter, Section, ContentChunk, ChatQuery, ChatResponse
- Relationships and foreign keys
- Validation rules from functional requirements

### API Contracts (contracts/)
- OpenAPI 3.1 specification for FastAPI endpoints
- RAG pipeline flow diagram and specifications

### Quickstart Guide (quickstart.md)
- Local development setup instructions
- Environment variable configuration
- How to run frontend and backend servers
- How to index chapters and test RAG pipeline

---

**Next Steps**: Execute Phase 0 (generate research.md) and Phase 1 (generate data-model.md, contracts/, quickstart.md).

**Branch**: `001-textbook-generation` (create from master)
**Implementation Plan Path**: `specs/textbook-generation/plan.md`
