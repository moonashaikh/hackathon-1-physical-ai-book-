from typing import List, Dict, Optional
import logging
from src.services.qdrant_service import qdrant_service
from src.services.pg_service import pg_service
from src.services.embedding_service import embedding_service

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

            # Generate a simple answer based on the context
            # In a real implementation, you would use a language model here
            answer = f"Based on the textbook content:\n\n{combined_context}\n\nFor your query '{query}', this is the relevant information from the textbook."

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

    def process_query(self, query: str, context_text: Optional[str] = None) -> Dict:
        """
        Process a query and return the response with source references
        """
        try:
            # Generate the answer
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