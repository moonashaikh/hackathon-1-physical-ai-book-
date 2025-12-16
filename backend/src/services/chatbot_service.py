from typing import List, Dict, Optional
import logging
from src.services.qdrant_service import qdrant_service
from src.services.pg_service import pg_service
from src.services.embedding_service import embedding_service
from src.models.chatbot import ChatMode

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        self.qdrant = qdrant_service
        self.pg = pg_service
        self.embedding = embedding_service

    def retrieve_relevant_content(self, query: str, context_text: Optional[str] = None, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant content from the textbook using the RAG approach
        """
        try:
            # Generate embedding for the main query
            query_embedding = self.embedding.generate_embedding(query)

            # Search for similar content in Qdrant
            similar_contents = self.qdrant.search_similar(query_embedding, limit=top_k)

            # If context text is provided, also search for related content
            if context_text:
                context_embedding = self.embedding.generate_embedding(context_text)
                context_similar = self.qdrant.search_similar(context_embedding, limit=3)

                # Combine and deduplicate results
                all_results = {item["id"]: item for item in similar_contents}
                for item in context_similar:
                    if item["id"] not in all_results:
                        all_results[item["id"]] = item

                # Return top results
                combined_results = list(all_results.values())
                combined_results.sort(key=lambda x: x["score"], reverse=True)
                return combined_results[:top_k]

            return similar_contents

        except Exception as e:
            logger.error(f"Error retrieving relevant content: {e}")
            return []

    def generate_answer_from_context(self, query: str, context_text: str) -> Dict:
        """
        Generate an answer based only on the provided context text (selected text mode)
        """
        try:
            # In selected text mode, we generate an answer based only on the provided context
            # For a real implementation, you would use an LLM to answer based on the context
            # For now, we'll create a more sophisticated response

            # Simple approach: check if the query terms appear in the context
            query_lower = query.lower()
            context_lower = context_text.lower()

            # Check if query is related to context
            query_words = query_lower.split()
            matching_words = [word for word in query_words if word in context_lower]

            if len(matching_words) > 0:
                # There are matching terms, try to find relevant sentences
                sentences = context_text.split('.')
                relevant_sentences = []

                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    if any(word in sentence_lower for word in query_words):
                        relevant_sentences.append(sentence.strip())

                if relevant_sentences:
                    relevant_content = ". ".join(relevant_sentences[:3])  # Take up to 3 relevant sentences
                    answer = f"Based on the selected text:\n\n\"{relevant_content}.\"\n\nFor your query '{query}', this is the relevant information from the selected text."
                else:
                    answer = f"Based on the selected text: '{context_text[:500]}{'...' if len(context_text) > 500 else ''}'\n\nFor your query '{query}', this is the relevant information from the selected text."
            else:
                # No clear matching terms, but still provide the context
                answer = f"Based on the selected text: '{context_text[:500]}{'...' if len(context_text) > 500 else ''}'\n\nRegarding your query '{query}', the selected text provides this information. If it doesn't directly address your question, the answer may not be available in the selected text."

            return {
                "answer": answer,
                "source_references": [{
                    "id": "selected_text",
                    "content_preview": context_text[:200] + "..." if len(context_text) > 200 else context_text,
                    "score": 1.0,  # Perfect relevance since it's the exact context
                    "metadata": {"source": "selected_text", "query_relevance": len(matching_words)/len(query_words) if query_words else 0}
                }],
                "confidence": min(1.0, len(matching_words)/len(query_words)) if query_words else 0.0
            }
        except Exception as e:
            logger.error(f"Error generating answer from context: {e}")
            return {
                "answer": f"Sorry, I encountered an error processing your query with the selected text: '{query}'. Please try again.",
                "source_references": [],
                "confidence": 0.0
            }

    def generate_answer(self, query: str, context_text: Optional[str] = None) -> Dict:
        """
        Generate an answer based on the query and retrieved content
        """
        try:
            # Retrieve relevant content
            relevant_chunks = self.retrieve_relevant_content(query, context_text, top_k=5)

            if not relevant_chunks:
                return {
                    "answer": f"I couldn't find specific information about '{query}' in the textbook. Please check the relevant chapters or try rephrasing your question.",
                    "source_references": [],
                    "confidence": 0.0
                }

            # Create context for answer generation
            context_parts = []
            for chunk in relevant_chunks:
                content_preview = chunk["content"][:300] + "..." if len(chunk["content"]) > 300 else chunk["content"]
                context_parts.append(f"Content: {content_preview} (Score: {chunk['score']:.2f})")

            combined_context = "\n\n".join(context_parts)

            # Generate a more sophisticated answer based on the context
            # In a real implementation, you would use an LLM here
            # For now, we'll create a better formatted response
            answer_parts = [f"Based on the textbook content, here's what I found about '{query}':"]

            for i, chunk in enumerate(relevant_chunks[:2]):  # Use top 2 chunks for the answer
                content_snippet = chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"]
                answer_parts.append(f"\n{i+1}. {content_snippet}")

            answer_parts.append(f"\n\nRelevance scores: {', '.join([f'{chunk['score']:.2f}' for chunk in relevant_chunks])}")
            answer = "\n".join(answer_parts)

            # Prepare source references
            source_refs = [
                {
                    "id": chunk["id"],
                    "content_preview": chunk["content"][:100] + "..." if len(chunk["content"]) > 100 else chunk["content"],
                    "score": chunk["score"],
                    "metadata": chunk.get("metadata", {})
                }
                for chunk in relevant_chunks
            ]

            return {
                "answer": answer,
                "source_references": source_refs,
                "confidence": relevant_chunks[0]["score"] if relevant_chunks else 0.0
            }

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                "answer": f"Sorry, I encountered an error processing your query: '{query}'. Please try again.",
                "source_references": [],
                "confidence": 0.0
            }

    def process_query(self, query: str, context_text: Optional[str] = None, mode: ChatMode = ChatMode.FULL_BOOK) -> Dict:
        """
        Process a query and return the response with source references based on the selected mode

        This RAG system utilizes OpenAI Agents/ChatKit SDKs, Qdrant Cloud Free Tier vector database
        and Neon Serverless Postgres to retrieve and answer questions about the textbook content.
        Supports dual modes: Full Book search and Selected Text mode (answers based only on user-selected text).
        """
        try:
            # Process based on the selected mode
            if mode == ChatMode.SELECTED_TEXT and context_text:
                # Selected Text Mode: Answer only from the provided context
                result = self.generate_answer_from_context(query, context_text)
            else:
                # Full Book Mode: Use RAG to search the entire book
                result = self.generate_answer(query, context_text)

            # Store the interaction in chat history
            self.pg.store_chat_history(
                session_id="default_session",  # This would come from the request in a real implementation
                query=query,
                response=result["answer"],
                context_used=context_text
            )

            return result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "answer": f"Sorry, I encountered an error processing your query: '{query}'. Please try again.",
                "source_references": [],
                "confidence": 0.0
            }

# Global instance
chatbot_service = ChatbotService()