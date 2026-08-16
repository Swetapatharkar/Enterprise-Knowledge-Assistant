from config import DOCUMENTS_PATH
from services.pdf_service import PDFService

pdf_service = PDFService()

for pdf in DOCUMENTS_PATH.glob("*.pdf"):

    print("=" * 60)

    print(pdf.name)

    text = pdf_service.read_pdf(pdf)

    print(text[:1000])