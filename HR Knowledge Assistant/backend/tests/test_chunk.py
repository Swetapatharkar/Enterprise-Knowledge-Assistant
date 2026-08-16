from config import DOCUMENTS_PATH
from services.pdf_service import PDFService
from services.chunk_service import ChunkService

pdf_service = PDFService()
chunk_service = ChunkService()

for pdf in DOCUMENTS_PATH.glob("*.pdf"):

    text = pdf_service.read_pdf(pdf)

    chunks = chunk_service.split_text(text)

    print(pdf.name)

    print("Chunks:", len(chunks))

    print(chunks[0])