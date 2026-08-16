from langchain_ollama import ChatOllama
import os

llm = ChatOllama(model="gemma3:1b")
print(llm.invoke("Hello").content)

print("OLLAMA_MODEL:", os.getenv("OLLAMA_MODEL"))
print("OLLAMA_HOST:", os.getenv("OLLAMA_HOST"))