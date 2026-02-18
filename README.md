<<<<<<< HEAD
# ChatBot
=======
# 🧠 PDF Insight Agent

An AI-powered document Q&A tool that lets you upload any PDF and ask questions about its content. Built with **RAG (Retrieval-Augmented Generation)**, it converts your documents into searchable vector embeddings and uses **Groq (Llama 3.3)** to deliver accurate, context-grounded answers.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat&logo=fastapi&logoColor=white)

---

## ✨ Features

- **PDF Upload** — Drag-and-drop any PDF via the sidebar.
- **Intelligent Chunking** — Splits documents into overlapping 1 000-character chunks for better retrieval.
- **Vector Search** — Uses [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) embeddings stored in a FAISS vector index.
- **RAG Pipeline** — Retrieves the top-3 most relevant chunks and sends them as context to the LLM.
- **Groq Llama 3.3** — Generates precise, context-aware answers with low temperature for factual accuracy.
- **Chat Interface** — Full conversational UI with message history, powered by Streamlit.

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────────────┐     ┌──────────────┐
│   PDF File   │────▶│  Text Chunking       │────▶│  Embeddings  │
│  (Upload)    │     │  (RecursiveCharSplit) │     │  (MiniLM)    │
└──────────────┘     └──────────────────────┘     └──────┬───────┘
                                                         │
                                                         ▼
┌──────────────┐     ┌──────────────────────┐     ┌──────────────┐
│   Answer     │◀────│  Groq (Llama 3.3)    │◀────│    FAISS     │
│  (Streamlit) │     │  (LLM Generation)    │     │  (Retrieval) │
└──────────────┘     └──────────────────────┘     └──────────────┘
```

---

## 📁 Project Structure

```
pdf_chatbot/
├── app.py              # Streamlit UI — sidebar upload, chat interface
├── rag_engine.py       # RAG backend — PDF loading, embeddings, LLM calls
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (ANTHROPIC_API_KEY)
└── .venv/              # Virtual environment
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- A [Groq API key](https://console.groq.com/keys)

### 1. Clone / Navigate to the Project

```bash
cd pdf_chatbot
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_...
```

### 5. Run the App

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## 🛠️ Usage

1. **Upload a PDF** using the sidebar file uploader.
2. Wait for the document to be processed (chunked & embedded).
3. **Ask questions** in the chat input at the bottom.
4. The agent retrieves relevant passages and generates an answer.
5. Use the sidebar buttons to **clear the conversation** or **reset the document**.

---

## ⚙️ Configuration

| Setting | Location | Default |
|---|---|---|
| Embedding model | `rag_engine.py` | `all-MiniLM-L6-v2` |
| Chunk size | `rag_engine.py` | `1000` characters |
| Chunk overlap | `rag_engine.py` | `200` characters |
| LLM model | `rag_engine.py` | `llama-3.3-70b-versatile` |
| Top-K retrieval | `rag_engine.py` | `3` chunks |
| Temperature | `rag_engine.py` | `0` |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
>>>>>>> 4bd46ee (project)
