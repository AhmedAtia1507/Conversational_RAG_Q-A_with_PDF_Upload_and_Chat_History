from RAG.VectorStore.VectorStoreClient import VectorStoreClient
from langchain_chroma import Chroma

class ChromaStore(VectorStoreClient):
    def __init__(self, embedding_function, persist_directory=".chroma/student_embeddings", top_k=5):
        self.embedding_function = embedding_function
        self.persist_directory = persist_directory
        self.vector_store = Chroma(embedding_function=embedding_function, persist_directory=persist_directory)
        self.top_k = top_k

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def retrieve(self, query_text):
        return self.vector_store.similarity_search(query_text, k=self.top_k)

    def persist(self):
        self.vector_store = Chroma(persist_directory=self.vector_store.persist_directory, embedding_function=self.vector_store.embedding_function)
    
    def as_retriever(self):
        return self.vector_store.as_retriever(kwargs={"k": self.top_k})