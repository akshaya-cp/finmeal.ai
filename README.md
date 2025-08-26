# 🚀 SmartLife.AI – Version 1

> 💡 **AI-powered Personal Finance & Meal Planning Assistant**
>
> This version implements a full-stack, modular Retrieval-Augmented Generation (RAG) pipeline using HuggingFace embeddings, FAISS vector store, LangChain, and FastAPI.

---

## 📌 Project Overview

SmartLife.AI is an intelligent assistant that helps users manage their **daily expenses** and receive **personalized meal plans**. It uses GenAI to answer queries with relevant, grounded responses retrieved from custom knowledge bases.

This repository includes:
- ✅ Backend with FastAPI for AI inference, RAG, and chat orchestration
- ✅ HuggingFace embeddings + FAISS for semantic document search
- ✅ Frontend powered by Streamlit for user interaction
- ✅ Modular agentic design with LangChain + LangGraph
- ✅ HuggingFace fallback support (no OpenAI dependency)

---

## 🏗️ Tech Stack

| Layer          | Stack / Tools |
|----------------|---------------|
| **Frontend**   | Streamlit     |
| **Backend**    | FastAPI       |
| **RAG Engine** | LangChain + LangGraph |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) |
| **Vector Store** | FAISS       |
| **LLMs**       | OpenAI (gpt-4o-mini), Groq (DeepSeek-70B) |
| **Infra**      | Localhost (v1), Render/Cloudflare ready |

---

## 📁 Folder Structure

smartlife_ai/
├── backend/
│   ├── ai_agent.py           # LangGraph + LangChain agent setup
│   ├── rag/
│   │   ├── loader.py         # Loads and splits documents
│   │   ├── vector_store.py   # FAISS vector store logic
│   │   ├── retriever.py      # HuggingFace retriever logic
│   └── main.py               # FastAPI backend entrypoint
├── frontend/
│   └── streamlit_app.py      # Frontend logic (Streamlit)
├── .gitignore
├── requirements.txt
├── README.md
└── test_env.py


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/your-username/smartlife_ai.git
cd smartlife_ai
```

### 🐍 Create and Activate Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it (depending on your OS)

# For Mac/Linux:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```

### Clone the Repo

```bash
git clone https://github.com/your-username/smartlife_ai.git
cd smartlife_ai
```

###  Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate      # for Mac/Linux
venv\Scripts\activate         # for Windows
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Start Backend Server (FastAPI)

```
cd backend
uvicorn main:app --host host_ip --port port_no. --reload
```
### Start Frontend UI (Streamlit)
#### open in another terminal

```bash
cd frontend
streamlit run streamlit_app.py
```




