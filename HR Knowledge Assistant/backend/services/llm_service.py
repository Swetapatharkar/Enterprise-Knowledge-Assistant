from langchain_openai import ChatOpenAI


class LLMService:

    def __init__(self):

        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0
        )

    def get_llm(self):

        return self.llm