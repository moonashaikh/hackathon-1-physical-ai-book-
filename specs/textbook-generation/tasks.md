# Tasks: Textbook Generation Feature

**Branch**: `1-ai-textbook-gen` | **Date**: 2025-12-05 | **Plan**: specs/textbook-generation/plan.md
**Input**: Feature specification from `specs/textbook-generation/spec.md`, Implementation Plan from `specs/textbook-generation/plan.md`, Data Model from `specs/textbook-generation/data-model.md`.

## Summary

This document provides an organized, actionable, and sequential breakdown of tasks for the "textbook-generation" feature. Tasks are designed to be small, executable, free-tier compatible, and focused on fast implementation with a clean structure, leading to a production-ready Docusaurus textbook with an integrated RAG chatbot.

## Dependencies

Tasks are ordered to reflect logical dependencies, ensuring foundational elements are in place before building complex features. User stories are largely independent after foundational tasks.

## Implementation Strategy

An MVP (Minimum Viable Product) approach will be used, prioritizing core textbook and RAG chatbot functionality first. Optional hooks will be implemented once the core features are stable and deployed.

## Phase 1: Setup

- [ ] T001 Create Docusaurus project structure `frontend/`
- [ ] T002 Initialize `frontend/docusaurus.config.js` with basic settings
- [ ] T003 Create FastAPI backend project structure `backend/`
- [ ] T004 Initialize `backend/main.py`
- [ ] T005 Create `backend/requirements.txt` with initial dependencies (fastapi, uvicorn, qdrant-client, psycopg2-binary, sentence-transformers)

## Phase 2: Foundational

- [ ] T006 Configure Qdrant client connection in `backend/app/db/qdrant_client.py`
- [ ] T007 Configure Neon Postgres client connection in `backend/app/db/pg_client.py`
- [ ] T008 Define Pydantic models for `Book`, `Chapter`, `Query`, `Response` in `backend/app/models/`
- [ ] T009 Implement database schema creation (tables for Book, Chapter) in `backend/app/db/schema.py`
- [ ] T010 Initialize lightweight embedding model (e.g., Sentence Transformers) in `backend/app/core/embeddings.py`

## Phase 3: User Story 1 - Docusaurus Textbook Content & UI

**Goal**: User can navigate a minimal Docusaurus textbook with basic content.
**Acceptance Criteria**: The Docusaurus site builds successfully and displays 6 chapters with correct navigation.

- [ ] T011 [P] [US1] Create `frontend/src/docs/chapter1.md` (Introduction to Physical AI)
- [ ] T012 [P] [US1] Create `frontend/src/docs/chapter2.md` (Basics of Humanoid Robotics)
- [ ] T013 [P] [US1] Create `frontend/src/docs/chapter3.md` (ROS 2 Fundamentals)
- [ ] T014 [P] [US1] Create `frontend/src/docs/chapter4.md` (Digital Twin Simulation)
- [ ] T015 [P] [US1] Create `frontend/src/docs/chapter5.md` (Vision-Language-Action Systems)
- [ ] T016 [P] [US1] Create `frontend/src/docs/chapter6.md` (Capstone: Simple AI-Robot Pipeline)
- [ ] T017 [US1] Configure `frontend/sidebar.js` for chapter navigation
- [ ] T018 [US1] Update `frontend/docusaurus.config.js` for sidebar and routing
- [ ] T019 [US1] Clean up default Docusaurus UI elements via `frontend/src/css/custom.css`
- [ ] T020 [US1] Apply minimal theme customizations in `frontend/src/theme/` (if needed)

## Phase 4: User Story 2 - RAG Chatbot Core Functionality

**Goal**: Backend API provides RAG capabilities based on textbook content.
**Acceptance Criteria**: API endpoints for `/embed`, `/query`, and `/chat` are functional and return appropriate responses.

- [ ] T021 [P] [US2] Implement `POST /embed` API endpoint in `backend/app/api/embed.py` to process and store chapter content embeddings in Qdrant and metadata in Neon Postgres
- [ ] T022 [P] [US2] Implement `POST /query` API endpoint in `backend/app/api/query.py` to retrieve relevant chunks from Qdrant and generate responses based on book content
- [ ] T023 [P] [US2] Implement `POST /chat` API endpoint in `backend/app/api/chat.py` for general RAG chatbot interaction
- [ ] T024 [US2] Integrate API routes into `backend/main.py`

## Phase 5: User Story 3 - Integrated Chatbot UI & Text-Selection Q&A

**Goal**: Users can interact with the RAG chatbot directly on the Docusaurus site and ask questions based on selected text.
**Acceptance Criteria**: Chatbot UI is functional, and text selection triggers a Q&A interaction with the backend.

- [ ] T025 [US3] Create `frontend/src/components/Chatbot.js` for the RAG chatbot UI
- [ ] T026 [US3] Integrate `Chatbot.js` into a Docusaurus layout or page (e.g., a dedicated chat page or sidebar component)
- [ ] T027 [US3] Implement client-side logic in Docusaurus to send selected text to `backend/api/query`
- [ ] T028 [US3] Display AI response for text-selection Q&A in the Docusaurus frontend

## Phase 6: Deployment & Optional Hooks

**Goal**: The Docusaurus textbook is deployed, and optional personalization/translation features are available.
**Acceptance Criteria**: The Docusaurus site is deployed to GitHub Pages and accessible. Optional buttons are present and functional (if implemented).

- [ ] T029 [US4] Configure Docusaurus for GitHub Pages deployment in `frontend/docusaurus.config.js`
- [ ] T030 [US4] Set up GitHub Actions workflow for automated Docusaurus build and deployment
- [ ] T031 [P] [US4] Implement "Personalize Chapter" button component and hook in `frontend/src/components/PersonalizeChapter.js`
- [ ] T032 [P] [US4] Implement "Urdu Translation" button component and hook in `frontend/src/components/UrduTranslation.js`

## Final Phase: Polish & Cross-Cutting Concerns

- [ ] T033 Implement comprehensive Pytest suite for `backend/` API endpoints
- [ ] T034 Implement Jest/React Testing Library tests for critical `frontend/` components
- [ ] T035 Review and optimize Docusaurus build process for speed
- [ ] T036 Final review of code for adherence to simplicity, consistency, and cost-efficiency principles
