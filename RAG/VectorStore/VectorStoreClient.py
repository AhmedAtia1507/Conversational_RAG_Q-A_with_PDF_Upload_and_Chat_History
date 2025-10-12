from abc import ABC, abstractmethod

class VectorStoreClient(ABC):
    """
    Abstract base class for vector store clients used in RAG (Retrieval-Augmented Generation) systems.
    This class defines the interface for vector store operations including document storage,
    similarity-based retrieval, persistence, and retriever functionality.
    Methods:
        add_documents(documents): Adds documents to the vector store for indexing and retrieval.
        retrieve(query_text, top_k=5): Performs similarity search to retrieve top-k most relevant documents.
        persist(): Saves the vector store state to persistent storage.
        as_retriever(): Returns a retriever object for integration with other components.
    Note:
        This is an abstract base class and cannot be instantiated directly.
        Concrete implementations must provide all abstract methods.
    """
    @abstractmethod
    def add_documents(self, documents):
        pass

    @abstractmethod
    def retrieve(self, query_text, top_k=5):
        pass

    @abstractmethod
    def persist(self):
        pass
    
    @abstractmethod
    def as_retriever(self):
        pass