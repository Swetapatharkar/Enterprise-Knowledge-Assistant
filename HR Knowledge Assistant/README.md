
# 🤖 HR Knowledge Assistant

An AI-powered **HR Knowledge Assistant** that answers questions from organizational HR documents using **Retrieval-Augmented Generation (RAG)** and a lightweight **Agentic AI** layer.

The system retrieves relevant information from HR documents, improves retrieval using reranking, and generates grounded answers with source citations.

---

## 🚀 Key Features

* 📄 PDF-based HR knowledge retrieval
* 🔎 FAISS vector search
* 🧠 Hugging Face CrossEncoder reranking
* ✨ Query rewriting for better retrieval
* 🤖 GPT-4.1 powered responses
* 🧩 Simple Agentic AI layer with one RAG tool
* 📚 Source and page citations
* 💬 Conversational chat interface
* ⚡ FastAPI backend
* 🎨 Streamlit frontend
* 🔐 Environment-based API key configuration

---

## 🏗️ Architecture

```text
                HR Documents / PDFs
                       │
                       ▼
              PDF Text Extraction
                       │
                       ▼
                Text Chunking
                       │
                       ▼
                Embeddings
                       │
                       ▼
              FAISS Vector Store
                       │
                       │
User Question ─────────┤
                       ▼
                Query Rewriting
                       │
                       ▼
              FAISS Retrieval
                       │
                       ▼
          CrossEncoder Reranking
                       │
                       ▼
                Relevant Context
                       │
                       ▼
                  RAG Service
                       │
                       ▼
                  GPT-4.1
                       │
                       ▼
                Agentic AI Layer
                       │
                       ▼
             FastAPI `/ask` API
                       │
                       ▼
               Streamlit UI
```

### Agentic AI

The agent is intentionally kept simple.

```text
User Question
      │
      ▼
   AI Agent
      │
      ▼
 HR RAG Tool
      │
      ▼
 Existing RAG Pipeline
      │
      ▼
 Grounded Answer + Sources
```

The agent uses the existing RAG pipeline as its **single tool**, demonstrating the core concept of Agentic AI without unnecessary complexity or multiple tools.

---

## 🔄 RAG Flow

1. HR documents are processed and converted into text chunks.
2. Chunks are converted into embeddings and stored in FAISS.
3. The user's question can be rewritten for better retrieval.
4. FAISS retrieves candidate documents.
5. A Hugging Face CrossEncoder reranks the retrieved documents.
6. The top relevant chunks are passed to GPT-4.1.
7. GPT-4.1 generates an answer using the retrieved context.
8. The system returns the answer along with document and page citations.

---

## 🛠️ Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Language        | Python                    |
| LLM             | OpenAI GPT-4.1            |
| Agent           | LangChain Tool Calling    |
| RAG             | LangChain                 |
| Vector Database | FAISS                     |
| Reranker        | Hugging Face CrossEncoder |
| Backend         | FastAPI                   |
| Frontend        | Streamlit                 |
| PDF Processing  | PyMuPDF                   |
| Embeddings      | Hugging Face              |
| Environment     | python-dotenv             |

---

## 📁 Project Structure

```text
HR Knowledge Assistant/
│
├── agents/
├── backend/
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── rag_service.py
│   │   ├── llm_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_service.py
│   │   ├── reranker_service.py
│   │   ├── query_rewriter_service.py
│   │   └── prompt_service.py
│   │
│   ├── main.py
│   └── tests/
│
├── documents/
├── frontend/
│   └── streamlit_app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ▶️ Running the Project

### 1. Create environment

```bash
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure API key

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key
```

### 3. Start FastAPI

From the `backend` directory:

```bash
uvicorn main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### 4. Start Streamlit

From the `frontend` directory:

```bash
streamlit run streamlit_app.py
```

---

## 🧪 Example

**Question:**

> How many weeks of maternity leave are provided?

**Answer:**

> Female employees are entitled to a maximum of 26 weeks (180 days) paid maternity leave. However, a woman with already two or more children is entitled to 12 weeks’ maternity leave.

**Source:** `Leave-Policy.pdf`, Page 3

---

## 🎯 Project Highlights

This project demonstrates practical implementation of:

**RAG → Retrieval Improvement → Reranking → Query Rewriting → LLM → Agentic AI → FastAPI → Streamlit**

The focus is on building a practical, explainable, and lightweight enterprise knowledge assistant rather than an unnecessarily complex agent system.

---

## 📌 Future Improvements

* Improved conversational memory
* Additional enterprise tools when required
* Authentication and authorization
* Production deployment
* Monitoring and evaluation
* Larger enterprise document collections
