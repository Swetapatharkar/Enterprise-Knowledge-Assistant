from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class VectorService:

    def create_vector_store(self, chunks, embedding_model):

        documents = []

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk["text"],
                    metadata={
                        "source": chunk["source"],
                        "page": chunk["page"]
                    }
                )
            )

        vector_store = FAISS.from_documents(
            documents,
            embedding_model
        )

        return vector_store


    def save_vector_store(self, vector_store, path):

        vector_store.save_local(path)


    def load_vector_store(self, path, embedding_model):

        return FAISS.load_local(
            path,
            embedding_model,
            allow_dangerous_deserialization=True
        )


    def search(self, vector_store, question, k=5):

      results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

      return results