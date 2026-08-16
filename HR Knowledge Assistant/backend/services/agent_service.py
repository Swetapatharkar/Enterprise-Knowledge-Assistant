import json

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from config import OPENAI_API_KEY
from services.rag_service import RAGService


class AgentService:

    def __init__(self):

        # Existing RAG system
        self.rag_service = RAGService()

        # Agent LLM
        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0,
            api_key=OPENAI_API_KEY
        )

        # Single Agent tool
        self.hr_rag_tool = self.create_rag_tool()

        # Give tool to Agent
        self.agent_llm = self.llm.bind_tools(
            [self.hr_rag_tool]
        )

    # --------------------------------------------------
    # HR RAG Tool
    # --------------------------------------------------

    def create_rag_tool(self):

        rag_service = self.rag_service

        @tool
        def hr_rag_tool(question: str) -> str:
            """
            Use this tool to answer questions about
            company HR policies and documents.
            """

            result = rag_service.answer_question(
                question,
                []
            )

            # Return complete RAG result
            # including answer and sources
            return json.dumps(result)

        return hr_rag_tool

    # --------------------------------------------------
    # Ask Agent
    # --------------------------------------------------

    def ask(self, question):

        response = self.agent_llm.invoke(
            [
                {
                    "role": "system",
                    "content": (
                        "You are an HR Knowledge Assistant agent. "
                        "For questions related to HR policies, "
                        "employee benefits, leave, insurance, "
                        "or company documents, use the HR RAG tool. "
                        "Do not answer HR policy questions from "
                        "your own knowledge."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        # --------------------------------------------------
        # Agent decided to use RAG
        # --------------------------------------------------

        if response.tool_calls:

            tool_call = response.tool_calls[0]

            tool_result = self.hr_rag_tool.invoke(
                tool_call["args"]
            )

            # Convert JSON string back to dictionary
            return json.loads(tool_result)

        # --------------------------------------------------
        # Agent did not use the tool
        # --------------------------------------------------

        return {
            "answer": response.content,
            "sources": []
        }