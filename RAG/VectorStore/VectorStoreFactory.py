import os
from langchain_huggingface import HuggingFaceEmbeddings
from RAG.Utils.ConfigReader import ConfigReader
from RAG.VectorStore.ChromaStore import ChromaStore

class VectorStoreFactory:
    """
    Factory class for creating vector store instances.
    This factory provides a centralized way to create vector store objects based on
    configuration settings. It currently supports Chroma vector stores and can be
    extended to support additional vector store types.
    The factory reads configuration from a ConfigReader and sets up the appropriate
    embedding model and vector store with the specified parameters.
    Raises:
        ValueError: If an unsupported vector store type is specified in the configuration.
    Example:
        >>> vector_store = VectorStoreFactory.create_vector_store()
        >>> # Returns a configured ChromaStore instance
    """
    @classmethod
    def create_vector_store(cls):
        config = ConfigReader().get("RAG", {})[0]
        vector_store_type = config.get("vector_store", "Chroma")
        embeddings = HuggingFaceEmbeddings(model_name=config.get("model_name", "bert-base-uncased"))

        available_vector_stores = ["Chroma"]
        if vector_store_type not in available_vector_stores:
            raise ValueError(f"Unknown vector store type: {vector_store_type}")
        
        top_k = config.get("top_k", 6)
        fetch_k = config.get("fetch_k", 20)
        lambda_mult = config.get("lambda_mult", 0.7)

        if vector_store_type == "Chroma":
            return ChromaStore(
                embedding_function=embeddings, 
                persist_directory=config.get("persist_directory", ".chroma/student_embeddings"), 
                top_k=top_k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult
            )
        raise ValueError(f"Unknown vector store type: {vector_store_type}")