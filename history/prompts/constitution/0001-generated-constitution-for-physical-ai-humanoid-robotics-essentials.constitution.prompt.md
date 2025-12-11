---
id: 0001
title: Generated Constitution for Physical AI & Humanoid Robotics — Essentials
stage: constitution
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["constitution", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: null
---

## Prompt

/sp.constitution

Project Name: Physical AI & Humanoid Robotics — Essentials
Continue. Generate the complete constitution.
Scope:
- Book will contain 6 short, focused chapters:
  1. Introduction to Physical AI
  2. Basics of Humanoid Robotics
  3. ROS 2 Fundamentals
  4. Digital Twin Simulation (Gazebo + Isaac)
  5. Vision-Language-Action Systems
  6. Capstone: Simple AI-Robot Pipeline
- Content must stay concise, accurate, and easy to understand.
- UI must be clean, modern, minimal, and fast.

Core Principles:
- Simplicity over complexity.
- Content must be correct, structured, and minimal.
- Free-tier-compatible architecture for embeddings and API usage.
- Avoid heavy GPU steps; prioritize lightweight design.
- RAG chatbot answers ONLY from book text.
- Consistent writing style and formatting across chapters.
- Fast build, clean structure, and production-safe code.

Key Features:
- Docusaurus-based textbook with clean layout.
- Integrated RAG chatbot (Qdrant + Neon + FastAPI).
- "Select text → Ask AI" interaction.
- Ready structure for:
  - Personalize Chapter button
  - Urdu Translation button
  - User profile–based content (optional)

Constraints:
- Minimal compute usage.
- Lightweight embeddings (for free tiers).
- Keep chapter size small and clean.

Success Criteria:
- Book builds successfully with no issues.
- RAG chatbot returns accurate answers from book content.
- UI looks clean, modern, and professional.
- Chapters are short, well-formatted, and aligned with course outcomes.
- Project deploys smoothly to GitHub Pages.

## Response snapshot

The project constitution for "Physical AI & Humanoid Robotics — Essentials" has been successfully generated and saved to .specify/memory/constitution.md. It defines the project's scope, core principles, key features, constraints, and success criteria.

## Outcome

- ✅ Impact: Constitution established for project guidance.
- 🧪 Tests: N/A
- 📁 Files: Constitution file created and updated.
- 🔁 Next prompts: Proceed with /sp.specify for feature specification.
- 🧠 Reflection: Successfully established foundational project principles and scope, aligning with user requirements for a Docusaurus-based book and RAG chatbot.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
