# Conversational RAG Q&A with PDF Upload and Chat History

## Overview

This project is an advanced conversational RAG (Retrieval-Augmented Generation) chatbot application that enables users to upload PDF documents and engage in intelligent multi-turn question-answering sessions. The application uses semantic chunking, MMR-based retrieval, and maintains chat history across multiple conversation threads for context-aware responses.

### Key Highlights

- **Semantic Chunking**: Uses gradient-based semantic boundaries for better context preservation
- **MMR Retrieval**: Maximum Marginal Relevance search for diverse, non-redundant results
- **Enhanced Embeddings**: High-quality 768-dimensional embeddings (all-mpnet-base-v2)
- **Hallucination Prevention**: Strict prompt engineering to ensure answers are grounded in source documents
- **Test Data Generator**: Synthetic PDF generator with ground-truth Q&A pairs for system validation

## Contents

```
Conversational_RAG_Q-A_with_PDF_Upload_and_Chat_History/
├── requirements.txt       # List of project dependencies
├── streamlit_app.py       # Main Streamlit application entry point
├── config.yaml            # Configuration for RAG settings (embeddings, chunking, retrieval)
├── pdf_generator.py       # Synthetic test PDF generator with ground-truth Q&A
├── app.log               # Application log file (generated at runtime)
├── .gitignore            # Git ignore rules (includes Test_Data/)
├── Test_Data/            # Generated test PDFs and Q&A pairs (created by pdf_generator.py)
│   ├── novatech_report.pdf
│   ├── quantum_lattice_paper.pdf
│   └── ground_truth_qa.txt
├── Engines/              # Chatbot engine implementations
│   ├── BaseChatbot.py    # Abstract base class for chatbot engines
│   └── RAG_Chatbot.py    # RAG-based chatbot implementation
└── RAG/                  # RAG pipeline and indexing modules
    ├── RAG_Pipeline.py   # Core RAG chain with LangChain and Groq
    ├── RAG_Indexing.py   # PDF processing with semantic chunking and metadata tracking
    ├── Utils/            # Utility modules
    │   └── ConfigReader.py
    └── VectorStore/      # Vector store implementations
        ├── VectorStoreClient.py   # Abstract base for vector stores
        ├── VectorStoreFactory.py  # Factory for creating vector stores
        └── ChromaStore.py         # Chroma vector store with MMR retrieval
```

## Key Features

### Core Capabilities
- **PDF Upload & Processing**: Upload PDF documents and ask questions based on their content
- **Semantic Chunking**: Intelligent text splitting using gradient-based breakpoints that preserve context
- **MMR Retrieval**: Maximum Marginal Relevance search to provide diverse, non-redundant answers
- **Conversational Interface**: Multi-turn conversations with maintained chat history per thread
- **Thread Management**: Create and switch between multiple independent chat threads
- **Cross-Document Support**: Metadata tracking enables questions across multiple uploaded PDFs

### Advanced Features
- **Hallucination Prevention**: Strict system prompts ensure answers are grounded in source documents
- **Enhanced Embeddings**: Uses `sentence-transformers/all-mpnet-base-v2` (768-dim) for high-quality semantic understanding
- **Optimized Retrieval**:
  - Retrieves top 6 chunks (k=6) for comprehensive coverage
  - Considers 20 candidates (fetch_k=20) before MMR filtering
  - Balances relevance and diversity (lambda_mult=0.7)
- **Multiple LLM Options**: Choose from different Groq models:
  - `openai/gpt-oss-120b`
  - `openai/gpt-oss-20b`
  - `llama-3.3-70b-versatile`
  - `gemma2-9b-it`

### Testing & Validation
- **Test Data Generator**: `pdf_generator.py` creates synthetic PDFs with ground-truth Q&A pairs
- **Comprehensive Test Suite**: Includes company reports, research papers, and 100+ test questions covering:
  - Simple fact retrieval
  - Multi-hop reasoning
  - List aggregation
  - Cross-document queries
  - Paraphrased questions
  - Ambiguous question handling
  - Hallucination trap questions

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages include:
- `streamlit` - Web interface
- `langchain` - RAG framework
- `langchain-experimental` - Semantic chunking
- `chromadb` - Vector database
- `sentence-transformers` - Embeddings
- `pypdf` - PDF processing
- `reportlab` - PDF generation (for test data)

### 2. Set Up API Key
Enter your Groq API key and HuggingFace API key in the Streamlit sidebar when the app starts.

### 3. Run the Application
```bash
streamlit run streamlit_app.py
```

### 4. Generate Test Data (Optional)
To create synthetic test PDFs:
```bash
python pdf_generator.py
```

This generates:
- `Test_Data/novatech_report.pdf` - Fictional company annual report
- `Test_Data/quantum_lattice_paper.pdf` - Fictional research paper
- `Test_Data/ground_truth_qa.txt` - 100+ test questions with answers

## Architecture

### Chat Flow
1. **PDF Upload** → `RAG_Indexing.index_pdf()` processes document:
   - Loads PDF using PyPDFLoader
   - Splits text using SemanticChunker with gradient-based breakpoints
   - Adds metadata (source_file, document_type) to each chunk
   - Generates embeddings and stores in ChromaDB

2. **Question Asked** → `RAG_Pipeline.stream()` generates response:
   - Retrieves relevant chunks using MMR search (balances relevance & diversity)
   - Includes chat history for context-aware follow-up questions
   - Applies strict system prompt to prevent hallucination
   - Streams response token-by-token for better UX

3. **Chat History** → Maintained per thread using LangChain's message history

### Configuration (`config.yaml`)
- **Embedding Model**: `sentence-transformers/all-mpnet-base-v2` (768-dimensional)
- **Vector Store**: ChromaDB with persistence at `.chroma/embeddings`
- **Chunking**: Semantic chunking with gradient-based breakpoints
- **Retrieval Configuration**:
  - `top_k: 6` - Number of final chunks to retrieve
  - `fetch_k: 20` - Candidate chunks to consider before MMR
  - `lambda_mult: 0.7` - Balance between relevance (1.0) and diversity (0.0)

## Technical Details

### Why Semantic Chunking?
Traditional character-based chunking can split text at arbitrary points, breaking semantic units. Semantic chunking uses embeddings to identify natural breakpoints where meaning shifts, resulting in:
- Better context preservation within chunks
- Improved retrieval accuracy
- More coherent answers

### Why MMR (Maximum Marginal Relevance)?
Standard similarity search can return redundant chunks (e.g., all from the same paragraph). MMR balances:
- **Relevance**: How well chunks match the query
- **Diversity**: How different chunks are from each other

This ensures the LLM receives diverse information, improving answer quality for complex questions.

## Testing Your RAG System

### Using Test Data
1. Generate test PDFs:
   ```bash
   python pdf_generator.py
   ```

2. Upload `Test_Data/novatech_report.pdf` and `Test_Data/quantum_lattice_paper.pdf` to the chatbot

3. Test with questions from `Test_Data/ground_truth_qa.txt`:
   ```
   # Simple fact retrieval
   Q: What was NovaTech's total revenue in 2024?
   Expected: $342.7M

   # Multi-hop reasoning
   Q: What is the difference between Q4 and Q1 revenue?
   Expected: $12.5M

   # Hallucination trap
   Q: What was NovaTech's Q5 2024 revenue?
   Expected: System should recognize Q5 doesn't exist
   ```

### Quality Metrics to Track
- **Accuracy**: Does the answer match ground truth?
- **Completeness**: For list questions, are all items retrieved?
- **Hallucination**: Does the system make up information?
- **Ambiguity Handling**: Does it ask for clarification when needed?
- **Cross-Document**: Can it answer questions spanning multiple PDFs?

## Logging

Application logs are written to `app.log` in this directory, capturing:
- Initialization events
- PDF upload and indexing operations
- Errors and exceptions with stack traces
- User interactions (questions asked, responses generated)

## License

This project is open source and available for educational and commercial use.
