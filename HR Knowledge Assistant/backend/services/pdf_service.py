import fitz
from pathlib import Path


class PDFService:

    def read_pdf(self, pdf_path: Path):
        """
        Read a PDF and return page-wise text with metadata.
        """

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            text = page.get_text()

            if text.strip():

                pages.append({
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_number
                })

        document.close()

        return pages