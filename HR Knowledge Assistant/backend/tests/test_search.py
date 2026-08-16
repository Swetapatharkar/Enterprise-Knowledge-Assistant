from config import VECTOR_DB_PATH

from services.embedding_service import EmbeddingService
from services.vector_service import VectorService

embedding_service = EmbeddingService()
vector_service = VectorService()

embedding_model = embedding_service.get_embedding_model()

vector_store = vector_service.load_vector_store(
    str(VECTOR_DB_PATH),
    embedding_model
)

question = input("Ask your question: ")

results = vector_service.search(
    vector_store,
    question
)

print("\nMost Relevant Chunks\n")

for i, (doc, score) in enumerate(results, start=1):

    print("=" * 70)
    print(f"Chunk {i}")

    print("Score:", score)
    print("Metadata:", doc.metadata)

    print("Source:", doc.metadata.get("source", "Unknown"))
    print("Page:", doc.metadata.get("page", "Unknown"))

    print("\nContent:")
    print(doc.page_content)

    print()