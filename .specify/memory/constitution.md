# Project Constitution: Physical AI & Humanoid Robotics — Essentials

## 1. Project Overview

**Project Name:** Physical AI & Humanoid Robotics — Essentials

**Description:** This project aims to create a concise, accurate, and easy-to-understand book on Physical AI and Humanoid Robotics, delivered via a Docusaurus-based platform. It will include an integrated RAG chatbot that answers questions based solely on the book's content.

## 2. Scope and Deliverables

### In Scope:
-   A Docusaurus-based textbook with a clean, modern, minimal, and fast UI.
-   Six short, focused chapters:
    1.  Introduction to Physical AI
    2.  Basics of Humanoid Robotics
    3.  ROS 2 Fundamentals
    4.  Digital Twin Simulation (Gazebo + Isaac)
    5.  Vision-Language-Action Systems
    6.  Capstone: Simple AI-Robot Pipeline
-   An integrated RAG chatbot powered by Qdrant, Neon, and FastAPI.
-   "Select text → Ask AI" interaction feature.
-   Ready structure for future features:
    -   "Personalize Chapter" button
    -   "Urdu Translation" button
    -   User profile–based content (optional)
-   Content must be concise, accurate, and easy to understand, adhering to a consistent writing style and formatting.

### Out of Scope:
-   Heavy GPU-dependent steps or components.
-   Complex, non-essential features that could increase computational cost or complexity.
-   Any AI chatbot responses that are not strictly derived from the book's text.

## 3. Core Principles

-   **Simplicity over Complexity:** Prioritize straightforward solutions and minimize intricate designs.
-   **Content Quality:** Ensure all content is correct, well-structured, and minimal, focusing on essential information.
-   **Cost Efficiency:** Design the architecture to be compatible with free tiers for embeddings and API usage.
-   **Lightweight Design:** Avoid heavy GPU usage; prioritize solutions that are computationally light.
-   **RAG Integrity:** The RAG chatbot must ONLY provide answers derived exclusively from the book's text.
-   **Consistency:** Maintain a consistent writing style and formatting across all chapters.
-   **Operational Excellence:** Aim for fast builds, clean project structure, and production-safe code.

## 4. Key Features

-   **Docusaurus Textbook:** A modern, clean, and minimal layout for optimal readability.
-   **Integrated RAG Chatbot:** Enables interactive Q&A based on book content.
-   **Contextual AI Interaction:** Allows users to select text and directly query the AI.
-   **Extensible Structure:** Pre-configured for easy addition of personalization, translation, and user-specific content features.

## 5. Constraints

-   **Minimal Compute Usage:** All components and processes should be designed to use as little computational resources as possible.
-   **Lightweight Embeddings:** Utilize embedding models suitable for free-tier usage.
-   **Chapter Size:** Chapters must remain small and focused to enhance readability and maintain conciseness.

## 6. Success Criteria

-   **Successful Build:** The book builds without any errors or warnings.
-   **Accurate RAG Chatbot:** The RAG chatbot consistently provides accurate answers based solely on the book's content.
-   **Clean UI:** The user interface is visually clean, modern, and professional.
-   **Content Alignment:** Chapters are short, well-formatted, and directly align with the stated course outcomes.
-   **Smooth Deployment:** The project deploys successfully to GitHub Pages with all features functional.