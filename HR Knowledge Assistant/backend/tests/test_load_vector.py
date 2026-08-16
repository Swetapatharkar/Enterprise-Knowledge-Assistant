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

print("Vector Store Loaded Successfully")