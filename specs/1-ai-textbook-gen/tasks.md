# Tasks: AI-Native Textbook Generation

**Feature Branch**: `1-ai-textbook-gen` | **Date**: 2025-12-05 | **Plan**: specs/1-ai-textbook-gen/plan.md

## Implementation Strategy

This implementation prioritizes a Minimum Viable Product (MVP) approach, focusing on delivering core textbook content and functional RAG chatbot interaction first. Subsequent features like personalization and translation will be integrated as optional hooks. Tasks are ordered to ensure foundational components are in place before building dependent features, with a strong emphasis on free-tier compatibility and efficient resource usage.

## Phase 1: Setup

**Goal**: Initialize the Docusaurus project and establish the basic frontend structure.

- [ ] T001 Create Docusaurus project in `frontend/`
- [ ] T002 Configure `docusaurus.config.js` for basic site metadata and plugin setup `frontend/docusaurus.config.js`
- [ ] T003 Set up initial Docusaurus folder structure: `frontend/docs/`, `frontend/src/components/`, `frontend/src/pages/`, `frontend/src/theme/`
- [ ] T004 Install frontend dependencies using `npm install` in `frontend/`

## Phase 2: Foundational (RAG Backend Setup)

**Goal**: Establish the core RAG chatbot backend with FastAPI, Qdrant, Neon Postgres, and embedding capabilities.

- [X] T005 Initialize FastAPI project in `backend/`
- [X] T006 Configure `.env` file for Qdrant and Neon Postgres connection details in `backend/.env`
- [X] T007 Set up Qdrant client connection logic in `backend/src/services/qdrant_service.py`
- [X] T008 Define Neon Postgres schema for metadata and create tables in `backend/src/models/database.py`
- [X] T009 Implement lightweight embedding generation service in `backend/src/services/embedding_service.py`
- [X] T010 Install backend dependencies using `pip install -r requirements.txt` in `backend/`

## Phase 3: User Story 1 - Read AI-Native Textbook [US1]

**Goal**: Enable users to access and read the textbook content with a clean UI and proper navigation.

**Independent Test**: The textbook website is accessible, displays all 6 chapters in the correct order, and allows navigation between them without errors. (SC-001)

- [X] T011 [US1] Create markdown file for "Chapter 1: Introduction to Physical AI" in `frontend/docs/chapter1.md`
- [X] T012 [P] [US1] Create markdown file for "Chapter 2: Basics of Humanoid Robotics" in `frontend/docs/chapter2.md`
- [X] T013 [P] [US1] Create markdown file for "Chapter 3: ROS 2 Fundamentals" in `frontend/docs/chapter3.md`
- [X] T014 [P] [US1] Create markdown file for "Chapter 4: Digital Twin Simulation (Gazebo + Isaac)" in `frontend/docs/chapter4.md`
- [X] T015 [P] [US1] Create markdown file for "Chapter 5: Vision-Language-Action Systems" in `frontend/docs/chapter5.md`
- [X] T016 [P] [US1] Create markdown file for "Chapter 6: Capstone: Simple AI-Robot Pipeline" in `frontend/docs/chapter6.md`
- [X] T017 [US1] Configure `frontend/sidebars.js` for auto-generated sidebar and routing based on `frontend/docs/`
- [X] T018 [US1] Customize Docusaurus theme (`frontend/src/theme/`) for minimalistic, modern, and beautiful UI
- [X] T019 [US1] Implement a basic Docusaurus homepage in `frontend/src/pages/index.js`

## Phase 4: User Story 2 - Interact with RAG Chatbot [US2]

**Goal**: Implement a fully functional RAG chatbot that answers questions based on textbook content, including text-selection Q&A.

**Independent Test**: The chatbot can be activated from any chapter, accepts text-based and text-selection-based queries, and provides accurate, in-scope answers derived only from the book. It politely declines out-of-scope questions. (SC-002, SC-003)

- [X] T020 [US2] Define Pydantic models for chatbot request and response in `backend/src/models/chatbot.py`
- [X] T021 [US2] Implement `POST /chat/query` endpoint in `backend/src/api/chatbot.py`
- [X] T022 [US2] Integrate Qdrant content retrieval logic into `backend/src/services/chatbot_service.py`
- [X] T023 [US2] Integrate Neon Postgres metadata retrieval for source references in `backend/src/services/chatbot_service.py`
- [X] T024 [US2] Implement answer generation logic using embeddings in `backend/src/services/chatbot_service.py`
- [X] T025 [US2] Create Chatbot UI React component in `frontend/src/components/Chatbot.js`
- [X] T026 [US2] Integrate Chatbot UI component into Docusaurus layout or specific pages `frontend/src/theme/Layout/index.js`
- [X] T027 [US2] Implement API client for `backend/chat/query` in `frontend/src/services/chatbot_api.js`
- [X] T028 [US2] Implement text selection event listener to capture context text in `frontend/src/components/Chatbot.js`
- [X] T029 [US2] Pass selected text as `context_text` to the `/chat/query` API endpoint

## Phase 5: User Story 3 - Personalize Chapter Content [US3]

**Goal**: Provide the structural hooks for chapter personalization.

**Independent Test**: The "Personalize Chapter" button appears on chapter pages and triggers a placeholder personalization workflow.

- [X] T030 [US3] Implement "Personalize Chapter" button (structure only) in `frontend/src/components/PersonalizeButton.js`
- [X] T031 [US3] Integrate `PersonalizeButton` into chapter pages/layout `frontend/src/theme/DocItem/Content/index.js`
- [X] T032 [US3] Define placeholder logic for personalization options in `frontend/src/services/personalization_service.js`

## Phase 6: User Story 4 - Translate Chapter [US4]

**Goal**: Provide the structural hooks for chapter translation into Urdu.

**Independent Test**: The "Translate to Urdu" button appears on chapter pages and triggers a placeholder translation workflow.

- [X] T033 [US4] Implement "Translate to Urdu" button (structure only) in `frontend/src/components/TranslateButton.js`
- [X] T034 [US4] Integrate `TranslateButton` into chapter pages/layout `frontend/src/theme/DocItem/Content/index.js`
- [X] T035 [US4] Define placeholder logic for translation service in `frontend/src/services/translation_service.js`

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Ensure the project is deployable, maintainable, and meets non-functional requirements.

- [X] T036 Configure GitHub Actions (`.github/workflows/deploy-docusaurus.yml`) for Docusaurus deployment to GitHub Pages
- [X] T037 Configure GitHub Actions (`.github/workflows/deploy-fastapi.yml`) for FastAPI backend deployment to a free-tier cloud service
- [X] T038 Add basic error handling and logging to FastAPI backend in `backend/src/main.py`
- [X] T039 Review and optimize Docusaurus build process for speed and minimalism in `frontend/docusaurus.config.js`
- [X] T040 Ensure all components operate within free-tier resource limits (review configurations and dependencies)
- [X] T041 Update `.gitignore` to exclude sensitive files and build artifacts in `.gitignore`

## Dependencies

- Phase 1 (Setup) -> Phase 2 (Foundational)
- Phase 2 (Foundational) -> Phase 4 (User Story 2 - Interact with RAG Chatbot)
- Phase 1 (Setup) -> Phase 3 (User Story 1 - Read AI-Native Textbook)
- Phase 3 (User Story 1) -> Phase 4 (User Story 2)
- Phase 3 (User Story 1) -> Phase 5 (User Story 3)
- Phase 3 (User Story 1) -> Phase 6 (User Story 4)
- All User Story Phases -> Phase 7 (Polish & Cross-Cutting Concerns)

## Parallel Execution Opportunities

- **Phase 3 [US1]**: Tasks T011-T016 (chapter creation) can be executed in parallel.
- **Within Phase 4 [US2]**: Backend API endpoint implementation (T021-T024) can largely be parallelized with frontend UI integration (T025-T027) once API contracts are stable.
- **Phases 5 [US3] and 6 [US4]**: These can be developed in parallel as they represent independent optional hooks.

## Suggested MVP Scope

For the initial MVP, focus on completing **Phase 1 (Setup)**, **Phase 2 (Foundational)**, **Phase 3 (User Story 1 - Read AI-Native Textbook)**, and **Phase 4 (User Story 2 - Interact with RAG Chatbot)**. This delivers the core textbook content with a functional, AI-powered Q&A system, providing significant user value and verifying the core technical architecture.