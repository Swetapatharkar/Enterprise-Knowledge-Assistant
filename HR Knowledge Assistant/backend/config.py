from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Project Root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# Documents Folder
# --------------------------------------------------

DOCUMENTS_PATH = PROJECT_ROOT / "documents"


# --------------------------------------------------
# FAISS Storage
# --------------------------------------------------

VECTOR_DB_PATH = PROJECT_ROOT / "vectorstore"


# --------------------------------------------------
# OpenAI API
# --------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")