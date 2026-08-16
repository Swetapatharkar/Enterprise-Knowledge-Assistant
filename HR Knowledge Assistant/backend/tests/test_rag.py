from services.rag_service import RAGService



# Create RAG Service
rag_service = RAGService()

print("=" * 60)
print("HR Knowledge Assistant")
print("=" * 60)

while True:

    question = input("\nAsk your question (type 'exit' to quit): ")

    if question.lower() == "exit":
        print("\nThank you for using HR Knowledge Assistant!")
        break

    response = rag_service.answer_question(question)

    print("\nAnswer:")
    print(response["answer"])

    print("\nSources:")

    for source in response["sources"]:

        print(f"- {source['source']} (Page {source['page']})")