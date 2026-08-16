from config import VECTOR_DB_PATH

from services.embedding_service import EmbeddingService
from services.vector_service import VectorService
from services.llm_service import LLMService
from services.prompt_service import PromptService
from services.reranker_service import RerankerService
from services.query_rewriter_service import QueryRewriterService


class RAGService:

    def __init__(self):

        # --------------------------------------------------
        # Initialize services
        # --------------------------------------------------

        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()
        self.llm_service = LLMService()
        self.prompt_service = PromptService()
        self.reranker_service = RerankerService()
        self.query_rewriter_service = QueryRewriterService()

        # --------------------------------------------------
        # Load embedding model
        # --------------------------------------------------

        self.embedding_model = (
            self.embedding_service.get_embedding_model()
        )

        # --------------------------------------------------
        # Load FAISS vector store
        # --------------------------------------------------

        self.vector_store = (
            self.vector_service.load_vector_store(
                str(VECTOR_DB_PATH),
                self.embedding_model
            )
        )

        # --------------------------------------------------
        # Initialize LLM and prompt
        # --------------------------------------------------

        self.llm = self.llm_service.get_llm()
        self.prompt = self.prompt_service.get_prompt()

    # --------------------------------------------------
    # Build retrieval query
    # --------------------------------------------------

    def build_retrieval_query(self, question, chat_history):

        return self.query_rewriter_service.rewrite(
            question,
            chat_history
        )

    # --------------------------------------------------
    # Answer question
    # --------------------------------------------------

    def answer_question(self, question, chat_history=None):

        if chat_history is None:
            chat_history = []

        # --------------------------------------------------
        # Format conversation history
        # --------------------------------------------------

        history_text = ""

        for message in chat_history:

            role = message.get("role", "")
            content = message.get("content", "").strip()

            if not content:
                continue

            if role == "user":

                history_text += f"User: {content}\n"

            elif role == "assistant":

                history_text += f"Assistant: {content}\n"

        # --------------------------------------------------
        # Rewrite question for retrieval
        # --------------------------------------------------

        retrieval_query = self.build_retrieval_query(
            question,
            chat_history
        )

        # --------------------------------------------------
        # Retrieve candidate documents using FAISS
        # --------------------------------------------------

        results = self.vector_service.search(
            self.vector_store,
            retrieval_query,
            k=5
        )

        # --------------------------------------------------
        # Extract documents
        # --------------------------------------------------

        documents = [
            doc for doc, score in results
        ]

        # --------------------------------------------------
        # Rerank documents using CrossEncoder
        # --------------------------------------------------

        reranked_results = self.reranker_service.rerank(
            retrieval_query,
            documents,
            top_n=3
        )

        # --------------------------------------------------
        # Build context
        # --------------------------------------------------

        context_parts = []

        for doc, score in reranked_results:

            context_parts.append(
                f"Source: {doc.metadata.get('source', 'Unknown')}\n"
                f"Page: {doc.metadata.get('page', 'Unknown')}\n"
                f"{doc.page_content}"
            )

        context = "\n\n".join(context_parts)

        # --------------------------------------------------
        # Create prompt
        # --------------------------------------------------

        messages = self.prompt.format_messages(
            context=context,
            question=question,
            chat_history=history_text
        )

        # --------------------------------------------------
        # Generate answer using GPT-4.1
        # --------------------------------------------------

        response = self.llm.invoke(messages)

        # --------------------------------------------------
        # Collect source citations
        # --------------------------------------------------

        sources = []

        for doc, score in reranked_results:

            sources.append({
                "source": doc.metadata.get(
                    "source",
                    "Unknown"
                ),
                "page": doc.metadata.get(
                    "page",
                    "Unknown"
                ),
                "score": float(score)
            })

        # --------------------------------------------------
        # Return final response
        # --------------------------------------------------

        return {
            "answer": response.content,
            "sources": sources
        }