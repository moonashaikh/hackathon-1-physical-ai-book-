# Data Model: Textbook Generation Feature

This document outlines the core entities, their fields, relationships, and validation rules for the textbook generation feature, derived from the feature specification.

## Entities

### 1. Book
*   **Description**: Represents the overall textbook project.
*   **Fields**:
    *   `id` (UUID): Primary Key.
    *   `title` (String): The title of the textbook (e.g., "Physical AI & Humanoid Robotics — Essentials").
    *   `description` (String): A brief description of the book.
    *   `creation_date` (Timestamp): When the book record was created.
    *   `last_updated_date` (Timestamp): When the book record was last modified.

### 2. Chapter
*   **Description**: Represents an individual chapter within the textbook.
*   **Fields**:
    *   `id` (UUID): Primary Key.
    *   `book_id` (UUID): Foreign Key referencing `Book.id`.
    *   `title` (String): The title of the chapter (e.g., "Introduction to Physical AI").
    *   `order` (Integer): The sequential order of the chapter within the book.
    *   `content_path` (String): The file path to the Markdown content of the chapter (e.g., `docs/chapter1.md`).
    *   `word_count` (Integer): The word count of the chapter content.
    *   `embedding_status` (Enum: `pending`, `processed`, `failed`): Status of the chapter's content processing for embeddings.
    *   `created_date` (Timestamp): When the chapter record was created.
    *   `last_updated_date` (Timestamp): When the chapter record was last modified.

### 3. Embedding (Conceptual / Qdrant Payload)
*   **Description**: Represents a vector embedding of a text segment from a chapter. Stored in Qdrant.
*   **Fields** (payload in Qdrant points):
    *   `chapter_id` (UUID): Reference to `Chapter.id`.
    *   `text_segment` (String): The original chunk of text that was embedded.
    *   `segment_start_char` (Integer): Starting character index of the segment in the original chapter content.
    *   `segment_end_char` (Integer): Ending character index of the segment in the original chapter content.
    *   `vector` (List[Float]): The actual embedding vector.

### 4. Query
*   **Description**: Represents a user's question or selected text for AI interaction.
*   **Fields**:
    *   `id` (UUID): Primary Key.
    *   `user_input` (String): The raw text of the user's question or selected content.
    *   `query_timestamp` (Timestamp): When the query was made.
    *   `chapter_context_id` (UUID, Optional): If the query originated from selected text within a specific chapter, references `Chapter.id`.

### 5. Response
*   **Description**: Represents the AI-generated answer to a user's query.
*   **Fields**:
    *   `id` (UUID): Primary Key.
    *   `query_id` (UUID): Foreign Key referencing `Query.id`.
    *   `response_text` (String): The AI's generated answer.
    *   `source_segments` (List[String]): A list of text segments from the book content that were used to formulate the answer.
    *   `response_timestamp` (Timestamp): When the response was generated.

### 6. Hook (Configuration / Feature Flag)
*   **Description**: Represents optional features that can be enabled/disabled.
*   **Fields**:
    *   `name` (String): Unique identifier for the hook (e.g., "Personalize Chapter", "Urdu Translation").
    *   `enabled` (Boolean): Flag indicating if the hook is active.

## Relationships

*   `Book` **has many** `Chapters` (one-to-many).
*   `Chapter` **produces many** `Embeddings` (one-to-many, conceptual through content processing).
*   `Query` **can be associated with one** `Chapter` (many-to-one, optional context).
*   `Query` **results in one** `Response` (one-to-one).

## Validation Rules

*   `Chapter` content (Markdown files) must be valid and conform to Docusaurus requirements.
*   The `order` field for `Chapter` must be unique within a given `book_id`.
*   RAG chatbot responses (`Response.response_text`) must strictly derive from `source_segments` within the book's content (enforcing RAG Integrity).
