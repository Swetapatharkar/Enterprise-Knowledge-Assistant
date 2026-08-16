import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

if key:
    print("OPENAI_API_KEY loaded successfully")
else:
    print("OPENAI_API_KEY NOT FOUND")