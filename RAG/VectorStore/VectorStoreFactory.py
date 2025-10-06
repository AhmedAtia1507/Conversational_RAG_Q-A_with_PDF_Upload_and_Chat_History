import yaml
import os
from langchain_huggingface import HuggingFaceEmbeddings
from RAG.Utils.ConfigReader import ConfigReader
from RAG.VectorStore.ChromaStore import ChromaStore

class VectorStoreFactory:
    @classmethod
    def create_vector_store(cls):
        config = ConfigReader().get("RAG", {})[0]
        vector_store_type = config.get("vector_store", "Chroma")
        if not os.environ.get("HF_TOKEN"):
            os.environ["HF_TOKEN"] = config.get("API_KEY", "")
        embeddings = HuggingFaceEmbeddings(model_name=config.get("model_name", "bert-base-uncased"))

        available_vector_stores = ["Chroma"]
        if vector_store_type not in available_vector_stores:
            raise ValueError(f"Unknown vector store type: {vector_store_type}")
        
        top_k = config.get("top_k", 5)
        if vector_store_type == "Chroma":
            return ChromaStore(embedding_function=embeddings, persist_directory=config.get("persist_directory", ".chroma/student_embeddings"), top_k=top_k)
        raise ValueError(f"Unknown vector store type: {vector_store_type}")