from services.llm_service import LLMService

llm = LLMService().get_llm()

response = llm.invoke("Say Hello")

print(response.content)