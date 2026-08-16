from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkService:

    def split_pages(self, pages):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = []

        for page in pages:

            split_texts = splitter.split_text(page["text"])

            for text in split_texts:

                chunks.append({
                    "text": text,
                    "source": page["source"],
                    "page": page["page"]
                })

        return chunks