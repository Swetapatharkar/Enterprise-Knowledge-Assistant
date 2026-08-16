from config import VECTOR_DB_PATH

from services.embedding_service import EmbeddingService
from services.vector_service import VectorService
from services.reranker_service import RerankerService


# --------------------------------------------------
# 1. Initialize services
# --------------------------------------------------

embedding_service = EmbeddingService()
vector_service = VectorService()
reranker_service = RerankerService()


# --------------------------------------------------
# 2. Load embedding model
# --------------------------------------------------

embedding_model = embedding_service.get_embedding_model()


# --------------------------------------------------
# 3. Load FAISS vector store
# --------------------------------------------------

vector_store = vector_service.load_vector_store(
    str(VECTOR_DB_PATH),
    embedding_model
)


# --------------------------------------------------
# 4. Get user question
# --------------------------------------------------

question = input("Ask your question: ")


# --------------------------------------------------
# 5. Retrieve candidates using FAISS
# --------------------------------------------------

results = vector_service.search(
    vector_store,
    question,
    k=5
)


# --------------------------------------------------
# 6. Extract Documents from FAISS results
# --------------------------------------------------

documents = [doc for doc, score in results]


# --------------------------------------------------
# 7. Print FAISS results
# --------------------------------------------------

print("\n" + "=" * 80)
print("FAISS RESULTS")
print("=" * 80)

for i, (doc, score) in enumerate(results, start=1):

    print(f"\nRank {i}")
    print(f"FAISS Score: {score}")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
    print(f"Page: {doc.metadata.get('page', 'Unknown')}")
    print(f"Content:\n{doc.page_content[:500]}")


# --------------------------------------------------
# 8. Rerank documents
# --------------------------------------------------

reranked_results = reranker_service.rerank(
    question,
    documents,
    top_n=3
)


# --------------------------------------------------
# 9. Print reranked results
# --------------------------------------------------

print("\n" + "=" * 80)
print("RERANKED RESULTS")
print("=" * 80)
if not reranked_results:

    print("\nNo sufficiently relevant documents found.")
else:

    for i, (doc, score) in enumerate(reranked_results, start=1):

            print(f"\nRank {i}")
            print(f"Reranker Score: {score:.4f}")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"Page: {doc.metadata.get('page', 'Unknown')}")
            print(f"Content:\n{doc.page_content[:500]}")

print("\n")