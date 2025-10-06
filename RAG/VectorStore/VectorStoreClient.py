from abc import ABC, abstractmethod

class VectorStoreClient(ABC):
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