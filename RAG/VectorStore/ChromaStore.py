from RAG.VectorStore.VectorStoreClient import VectorStoreClient
from langchain_chroma import Chroma

class ChromaStore(VectorStoreClient):
    """
    A vector store implementation using ChromaDB for document storage and retrieval.
    This class provides a wrapper around ChromaDB's Chroma vector store, implementing
    the VectorStoreClient interface for document embedding, storage, and similarity search.
    Attributes:
        embedding_function: Function used to generate embeddings for documents and queries
        persist_directory (str): Directory path where the ChromaDB data is persisted
        vector_store (Chroma): The underlying ChromaDB vector store instance
        top_k (int): Number of top similar documents to retrieve in searches
    Args:
        embedding_function: The embedding function to use for vectorizing text
        persist_directory (str, optional): Directory for persisting the vector store. 
            Defaults to ".chroma/student_embeddings"
        top_k (int, optional): Number of top results to return in similarity searches. 
            Defaults to 5
    Methods:
        add_documents(documents): Add documents to the vector store
        retrieve(query_text): Perform similarity search and return top-k documents
        persist(): Reinitialize the vector store from persisted data
        as_retriever(): Return a retriever interface for the vector store
    """
    def __init__(self, embedding_function, persist_directory=".chroma/student_embeddings", top_k=6, fetch_k=20, lambda_mult=0.7):
        self.embedding_function = embedding_function
        self.persist_directory = persist_directory
        self.vector_store = Chroma(embedding_function=embedding_function, persist_directory=persist_directory)
        self.top_k = top_k
        self.fetch_k = fetch_k
        self.lambda_mult = lambda_mult

    def add_documents(self, documents):
        """
        Add documents to the vector store.

        This method adds a collection of documents to the ChromaDB vector store,
        where they will be embedded and indexed for similarity search operations.

        Args:
            documents (list): A list of document objects to be added to the vector store.
                             Each document should contain text content and optional metadata.

        Returns:
            None

        Raises:
            Exception: If there's an error during the document addition process.

        Example:
            >>> chroma_store = ChromaStore()
            >>> docs = [Document(page_content="Sample text", metadata={"source": "file.pdf"})]
            >>> chroma_store.add_documents(docs)
        """
        self.vector_store.add_documents(documents)

    def retrieve(self, query_text):
        """
        Retrieve the most similar documents from the vector store based on a query.

        This method performs a similarity search on the stored document vectors to find
        the top-k most relevant documents that match the given query text.

        Args:
            query_text (str): The input text query to search for similar documents.

        Returns:
            list: A list of the top-k most similar documents from the vector store,
                  ordered by similarity score (most similar first).

        Note:
            The number of returned documents is controlled by the self.top_k parameter
            set during initialization of the ChromaStore instance.
        """
        return self.vector_store.similarity_search(query_text, k=self.top_k)

    def persist(self):
        """
        Persists the current vector store to disk.
        
        This method reinitializes the Chroma vector store with the same persist directory
        and embedding function to ensure the current state is saved to persistent storage.
        The vector store will be available for future sessions after calling this method.
        
        Returns:
            None
        """
        self.vector_store = Chroma(persist_directory=self.vector_store.persist_directory, embedding_function=self.vector_store.embedding_function)
    
    def as_retriever(self):
        """
        Convert the vector store to a retriever object.

        Returns:
            Retriever: A retriever object configured with the specified top_k parameter
            for similarity search. The retriever can be used to find the most relevant
            documents based on query similarity.
        """
        return self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": self.top_k,
                "fetch_k": self.fetch_k,
                "lambda_mult": self.lambda_mult
            }
        )