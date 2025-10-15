import os
import gc
import sys
import traceback
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from RAG.VectorStore.VectorStoreFactory import VectorStoreFactory
from RAG.Utils.ConfigReader import ConfigReader
from streamlit.runtime.uploaded_file_manager import UploadedFile

class RAG_Indexing:
    """
        RAG_Indexing provides functionality for indexing PDF documents into a Chroma vector store using HuggingFace embeddings.
        Attributes:
            config (dict): Configuration parameters loaded from Utils.ConfigReader for RAG operations.
            embeddings (HuggingFaceEmbeddings): Embedding model used to generate vector representations of text.
            vector_store (Chroma): Chroma vector store instance for persisting and retrieving document embeddings.
        Methods:
            __init__(persist_directory=".chroma/student_embeddings"):
                Initializes the RAG_Indexing instance, sets up configuration, environment variables, HuggingFace embeddings, and Chroma vector store.
            index_pdf(pdf_path):
                pdf_path (str): Path to the PDF document to be indexed.
                Exceptions from PyPDFLoader, RecursiveCharacterTextSplitter, or vector_store.add_documents.
    """
    def __init__(self, config_file="config.yaml"):
        """
            Initializes the RAG_Indexing class.

            Sets up configuration, environment variables, HuggingFace embeddings, and initializes the Chroma vector store.
        """
        self.config = ConfigReader(config_file=config_file)
        self.config = self.config.get("RAG", {})[0]
        self.embeddings = HuggingFaceEmbeddings(model_name=self.config.get("model_name", "bert-base-uncased"))
        self.vector_store = VectorStoreFactory.create_vector_store()

    def index_pdf(self, pdf_path):
        """
        Indexes a PDF file by loading its contents, splitting the text into chunks, and adding the chunks to the vector store.

        Args:
            pdf_path (str): The file path to the PDF document to be indexed.

        Process:
            - Loads the PDF document using PyPDFLoader.
            - Retrieves chunking configuration from self.config.
            - Splits the document into text chunks using RecursiveCharacterTextSplitter with specified chunk size and overlap.
            - Adds the resulting text chunks to the vector store for retrieval.

        Raises:
            Any exceptions raised by PyPDFLoader, RecursiveCharacterTextSplitter, or vector_store.add_documents.
        """
        try:
            # Case 1: If user passes a Streamlit UploadedFile
            print("pdf_path type:", type(pdf_path))
            temp_file_path = None
            if isinstance(pdf_path, UploadedFile):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(pdf_path.read())
                    temp_file_path = tmp_file.name
            elif isinstance(pdf_path, str):
                temp_file_path = pdf_path
            elif isinstance(pdf_path, (bytes, bytearray)):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(pdf_path)
                    temp_file_path = tmp_file.name
            else:
                raise ValueError("index_pdf expects either a file path (str), a Streamlit UploadedFile, or raw bytes")

            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()
            # Extract filename for metadata tracking
            filename = os.path.basename(temp_file_path)
            # Remove temp file prefixes if present
            if filename.startswith('tmp'):
                # Try to get original filename from UploadedFile
                if isinstance(pdf_path, UploadedFile):
                    filename = pdf_path.name

            semantic_splitter = SemanticChunker (
                embeddings=self.embeddings,
                breakpoint_threshold_type="gradient",
                breakpoint_threshold_amount=1
            )
            texts = semantic_splitter.split_documents(documents)

            if not texts:
                print("Warning: No text chunks to index. The PDF may be empty or unreadable.")
                return

            # Add metadata to each chunk for cross-document tracking
            for text in texts:
                text.metadata["source_file"] = filename
                text.metadata["document_type"] = "pdf"

            self.vector_store.add_documents(texts)
        except Exception as e:
            print(f"Error during PDF indexing: {e}", file=sys.stderr)
            traceback.print_exc()
        finally:
            # Clean up temp files and force garbage collection
            try:
                if 'temp_file_path' in locals() and temp_file_path and temp_file_path != pdf_path and isinstance(temp_file_path, str):
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
            except Exception as cleanup_err:
                print(f"Error cleaning up temp file: {cleanup_err}", file=sys.stderr)
            gc.collect()
    
    def get_retriever(self):
        """
        Returns a retriever object from the vector store with optimized configuration.

        This method creates and returns a retriever interface configured with:
        - MMR (Maximum Marginal Relevance) search for diversity
        - k=6 to retrieve enough chunks for list/aggregation questions
        - fetch_k=20 to consider more candidates before MMR filtering
        - lambda_mult=0.7 to balance relevance and diversity

        Returns:
            Retriever: A retriever object that provides an interface for
                      querying the vector store and retrieving relevant documents.
        """
        return self.vector_store.as_retriever()
