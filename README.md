# Conversational RAG Q&A with PDF Upload and Chat History

## Overview

This project is a conversational RAG (Retrieval-Augmented Generation) chatbot application that enables users to upload PDF documents and engage in multi-turn question-answering sessions. The application maintains chat history across multiple conversation threads, allowing for context-aware responses based on the uploaded documents.

## Contents

```
Conversational_RAG_Q-A_with_PDF_Upload_and_Chat_History/
├── streamlit_app.py       # Main Streamlit application entry point
├── config.yaml            # Configuration for RAG settings
├── app.log               # Application log file (generated at runtime)
├── Engines/              # Chatbot engine implementations
│   ├── BaseChatbot.py    # Abstract base class for chatbot engines
│   └── RAG_Chatbot.py    # RAG-based chatbot implementation
└── RAG/                  # RAG pipeline and indexing modules
    ├── RAG_Pipeline.py   # Core RAG chain with LangChain and Groq
    ├── RAG_Indexing.py   # PDF processing and vector store indexing
    ├── Utils/            # Utility modules
    │   └── ConfigReader.py
    └── VectorStore/      # Vector store implementations
        ├── VectorStoreClient.py   # Abstract base for vector stores
        ├── VectorStoreFactory.py  # Factory for creating vector stores
        └── ChromaStore.py         # Chroma vector store implementation
```

## Key Features

- **PDF Upload & Processing**: Upload PDF documents and ask questions based on their content
- **Conversational Interface**: Multi-turn conversations with chat history per thread
- **Thread Management**: Create and switch between multiple chat threads
- **Multiple LLM Options**: Choose from different Groq models:
  - `openai/gpt-oss-120b`
  - `openai/gpt-oss-20b`
  - `llama-3.3-70b-versatile`
  - `gemma2-9b-it`
- **Vector Store**: Uses ChromaDB for document embeddings and retrieval

## How to Run

```bash
streamlit run streamlit_app.py
```

**Requirements:**
- A valid Groq API key (enter in the sidebar when the app starts)
- Python dependencies from `requirements.txt` in parent directory

## Architecture

### Chat Flow
1. User uploads PDF → `RAG_Indexing.index_pdf()` processes and stores embeddings in ChromaDB
2. User asks question → `RAG_Pipeline.stream()` retrieves relevant context and generates response
3. Chat history is maintained per thread using LangChain's message history

### Configuration (`config.yaml`)
- **Embedding Model**: `all-MiniLM-L6-v2` (HuggingFace)
- **Vector Store**: ChromaDB with persistence at `.chroma/embeddings`
- **Chunking**: 500 character chunks with 100 character overlap
- **Retrieval**: Top 5 most relevant chunks

## Logging

Application logs are written to `app.log` in this directory, capturing initialization events, errors, and user interactions.
