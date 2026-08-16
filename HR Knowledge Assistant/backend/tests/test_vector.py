from config import DOCUMENTS_PATH, VECTOR_DB_PATH

from services.pdf_service import PDFService
from services.chunk_service import ChunkService
from services.embedding_service import EmbeddingService
from services.vector_service import VectorService


pdf_service = PDFService()
chunk_service = ChunkService()
embedding_service = EmbeddingService()
vector_service = VectorService()


all_chunks = []


for pdf in DOCUMENTS_PATH.glob("*.pdf"):

    print(f"Processing: {pdf.name}")

    pages = pdf_service.read_pdf(pdf)

    chunks = chunk_service.split_pages(pages)

    all_chunks.extend(chunks)


print(f"Total chunks created: {len(all_chunks)}")


# Create embedding model
embedding_model = embedding_service.get_embedding_model()


# Create FAISS vector store
vector_store = vector_service.create_vector_store(
    all_chunks,
    embedding_model
)


# Save vector database
vector_service.save_vector_store(
    vector_store,
    str(VECTOR_DB_PATH)
)


print("Vector Store Saved Successfully")