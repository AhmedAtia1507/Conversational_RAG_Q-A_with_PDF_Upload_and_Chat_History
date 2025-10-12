import gc
import sys
import traceback
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
            chunking_configs = self.config.get("Chunking", [{}])

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunking_configs.get("chunk_size", 500),
                chunk_overlap=chunking_configs.get("chunk_overlap", 100)
            )
            texts = text_splitter.split_documents(documents)
            if not texts:
                print("Warning: No text chunks to index. The PDF may be empty or unreadable.")
                return
            self.vector_store.add_documents(texts)
        except Exception as e:
            print(f"Error during PDF indexing: {e}", file=sys.stderr)
            traceback.print_exc()
        finally:
            # Clean up temp files and force garbage collection
            try:
                if 'temp_file_path' in locals() and temp_file_path and temp_file_path != pdf_path and isinstance(temp_file_path, str):
                    import os
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
            except Exception as cleanup_err:
                print(f"Error cleaning up temp file: {cleanup_err}", file=sys.stderr)
            gc.collect()
    
    def get_retriever(self):
        """
        Returns a retriever object from the vector store.
        
        This method creates and returns a retriever interface that can be used
        to search and retrieve relevant documents from the vector store based
        on similarity search queries.
        
        Returns:
            Retriever: A retriever object that provides an interface for
                      querying the vector store and retrieving relevant documents.
        """
        return self.vector_store.as_retriever()
# # Testing the RAG_Indexing class
# if __name__ == "__main__":
#     rag_indexing = RAG_Indexing()
#     config_path = os.path.join(os.path.dirname(__file__), "ShellIntro.pdf")
#     rag_indexing.index_pdf(config_path)