# Implementation Plan: textbook-generation

**Branch**: `1-ai-textbook-gen` | **Date**: 2025-12-05 | **Spec**: specs/textbook-generation/spec.md
**Input**: Feature specification from `/specs/textbook-generation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The "textbook-generation" feature aims to create a Docusaurus-based online textbook on Physical AI and Humanoid Robotics, including an integrated RAG chatbot. The chatbot will be powered by a FastAPI backend, Qdrant for vector storage, Neon Postgres for metadata, and lightweight embeddings, providing text-selection-based Q&A strictly from the book's content. The plan focuses on a clean, minimal, and modern UI, with free-tier compatibility and an extensible structure for future personalization and translation hooks.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+ (for FastAPI), Node.js (for Docusaurus)
**Primary Dependencies**: Docusaurus, FastAPI, Qdrant, Neon Postgres, lightweight embedding library (e.g., Sentence Transformers with a small model)
**Storage**: Qdrant (vector store for embeddings), Neon Postgres (metadata for textbook content and RAG index)
**Testing**: Pytest (for FastAPI backend), Jest and React Testing Library (for Docusaurus frontend)
**Target Platform**: GitHub Pages (for Docusaurus frontend deployment), Cloud platform compatible with free-tier (for FastAPI backend - e.g., Render, Vercel for serverless if applicable, or similar)
**Project Type**: Web application (Docusaurus frontend + FastAPI backend)
**Performance Goals**: Fast builds, efficient API responses (low latency for RAG queries), minimal resource consumption for free-tier compatibility.
**Constraints**: Minimal compute usage, lightweight embeddings, 6 short and focused chapters, RAG chatbot must ONLY provide answers derived exclusively from the book's text.
**Scale/Scope**: 6 short chapters, integrated RAG chatbot, text-selection-based Q&A, optional "Personalize Chapter" and "Urdu Translation" buttons (hooks).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**1. Simplicity over Complexity:** Prioritize straightforward solutions and minimize intricate designs.
   - **Check**: The plan emphasizes minimal design and free-tier compatibility, aligning with this principle. (PASS)

**2. Content Quality:** Ensure all content is correct, well-structured, and minimal, focusing on essential information.
   - **Check**: The plan includes a chapter creation workflow and consistent formatting, addressing content quality. (PASS)

**3. Cost Efficiency:** Design the architecture to be compatible with free tiers for embeddings and API usage.
   - **Check**: Explicitly using lightweight embeddings and free-tier compatible services. (PASS)

**4. Lightweight Design:** Avoid heavy GPU usage; prioritize solutions that are computationally light.
   - **Check**: Focus on lightweight embeddings and minimal compute usage. (PASS)

**5. RAG Integrity:** The RAG chatbot must ONLY provide answers derived exclusively from the book's text.
   - **Check**: The RAG chatbot architecture and workflow will be designed to enforce this. (PASS)

**6. Consistency:** Maintain a consistent writing style and formatting across all chapters.
   - **Check**: The chapter creation workflow will include guidelines for consistency. (PASS)

**7. Operational Excellence:** Aim for fast builds, clean project structure, and production-safe code.
   - **Check**: The plan includes build, test, and deployment steps for GitHub Pages, focusing on speed and clean structure. (PASS)

## Project Structure

### Documentation (this feature)

```text
specs/textbook-generation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── docusaurus.config.js
├── src/
│   ├── pages/         # Custom pages
│   ├── components/    # Reusable React components
│   ├── css/           # Custom CSS for styling
│   ├── theme/         # Docusaurus theme overrides
│   └── docs/          # Markdown files for chapters
│       ├── chapter1.md
│       ├── chapter2.md
│       └── ...
├── static/            # Static assets
└── blog/              # (Remove if not used)
└── sidebar.js         # Docusaurus sidebar configuration

backend/
├── main.py            # FastAPI application entry point
├── app/
│   ├── api/           # API routes (e.g., chatbot, Q&A)
│   ├── core/          # Core logic (embeddings, RAG process)
│   ├── db/            # Database interactions (Qdrant, Neon Postgres)
│   └── models/        # Pydantic models for data validation
├── requirements.txt   # Python dependencies
└── tests/             # Backend tests
```

**Structure Decision**: The project will adopt a split `frontend/` and `backend/` structure. The `frontend/` directory will house the Docusaurus application, including configuration, custom components, styling, and the Markdown content for the textbook chapters. The `backend/` directory will contain the FastAPI application, responsible for the RAG chatbot, API endpoints, and database interactions with Qdrant and Neon Postgres. This separation allows for independent development and deployment of each component.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |
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
