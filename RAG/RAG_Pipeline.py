import os
from RAG.RAG_Indexing import RAG_Indexing
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

class RAG_Pipeline:
    """
    A Retrieval-Augmented Generation (RAG) pipeline for processing PDF documents and answering questions.
    This class implements a complete RAG system that combines document retrieval with language model generation
    to provide contextually relevant answers based on uploaded PDF content. It maintains conversation history
    per session and supports streaming responses.
    Attributes:
        llm (ChatGroq): The language model instance for generating responses
        history (dict): Dictionary mapping session IDs to ChatMessageHistory objects
        rag_indexing (RAG_Indexing): Component responsible for document indexing and retrieval
        promptTemplate (ChatPromptTemplate): Template for formatting prompts with context and history
        ragChain: The composed chain for RAG processing
        chain (RunnableWithMessageHistory): The main execution chain with message history support
    Methods:
        get_session_history(session_id): Retrieves or creates chat history for a session
        stream(session_id, user_input): Streams responses for user queries with context retrieval
        clear_session_history(session_id): Clears conversation history for a specific session
        change_llm_type(model_name): Changes the underlying language model
        get_llm_type(): Returns the current language model name
        processPDF(pdf_path): Processes and indexes a PDF document for retrieval
    Example:
        >>> rag = RAG_Pipeline()
        >>> rag.processPDF("document.pdf")
        >>> for chunk in rag.stream("session_1", "What is the main topic?"):
        ...     print(chunk, end="")
    """
    def __init__(self, model_name="openai/gpt-oss-120b"):
        self.llm = ChatGroq(model_name=model_name, api_key=os.environ["GROQ_API_KEY"], streaming=True)
        self.history = {} # maps session_id to ChatMessageHistory
        self.rag_indexing = RAG_Indexing()
        self.promptTemplate = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the user's question based on the context provided."),
            ("system", "Relevant Context: {Context}"),
            MessagesPlaceholder(variable_name="History"),
            ("human", "{Question}")
        ])
        # Compose the RAG chain step by step for clarity
        self.ragChain = (
            self.promptTemplate  # Format prompt with context and history
            | self.llm  # Generate response using the language model
            | StrOutputParser()  # Parse the output to string
        )
        self.chain = RunnableWithMessageHistory (
            self.ragChain,
            self.get_session_history,
            input_messages_key="Question",
            history_messages_key="History"
        )
    
    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        """
        Retrieve or create a chat message history for a given session.

        This method implements a session-based chat history management system where each
        session is identified by a unique session ID. If a session doesn't exist, it
        creates a new ChatMessageHistory instance for that session.

        Args:
            session_id (str): Unique identifier for the chat session. Used to retrieve
                             or create the corresponding message history.

        Returns:
            ChatMessageHistory: The chat message history object associated with the
                               given session_id. Contains all previous messages for
                               this particular session.

        Note:
            - If the session_id doesn't exist in self.history, a new ChatMessageHistory
              instance is created and stored.
            - This enables maintaining separate conversation contexts for different users
              or conversation threads.
        """
        if session_id not in self.history:
            self.history[session_id] = ChatMessageHistory()
        return self.history[session_id]
    
    def stream(self, session_id: str, user_input: str):
        """
        Stream responses from the RAG pipeline for a given user input.
        
        This method retrieves relevant context using the RAG indexing system and then
        generates streaming responses using the configured chain. If streaming is not
        supported by the chain, it falls back to returning the full response.
        
        Args:
            session_id (str): Unique identifier for the conversation session to maintain
                             chat history and context.
            user_input (str): The user's question or input text to process.
        
        Yields:
            str or dict: Streaming chunks of the generated response if the chain supports
                        streaming, otherwise yields the complete response. In case of errors,
                        yields error messages as strings.
        
        Raises:
            Exception: Catches and yields error messages for both context retrieval
                      and response generation failures.
        
        Note:
            This method handles errors gracefully by yielding error messages instead
            of raising exceptions, ensuring the streaming interface remains stable.
        """
        try:
            related_context = self.rag_indexing.get_retriever().invoke(user_input)
        except Exception as e:
            yield f"Error retrieving context: {e}"
            return
        try:
            # If chain supports streaming, yield chunks
            if hasattr(self.chain, "stream"):
                for chunk in self.chain.stream(
                    {"Question": user_input, "Context": related_context},
                    config={"configurable": {"session_id": session_id}}
                ):
                    if chunk:
                        yield chunk
            else:
                # Fallback: return full response
                response = self.chain.invoke(
                    {"Question": user_input, "Context": related_context},
                    config={"configurable": {"session_id": session_id}}
                )
                yield response
        except Exception as e:
            yield f"Error generating response: {e}"

    def clear_session_history(self, session_id: str):
        """
        Clear the chat history for a specific session.

        This method removes all stored conversation history associated with the given
        session ID from the history dictionary. If the session ID doesn't exist,
        the method will silently do nothing.

        Args:
            session_id (str): The unique identifier for the session whose history
                             should be cleared.

        Returns:
            None

        Example:
            >>> rag_pipeline = RAGPipeline()
            >>> rag_pipeline.clear_session_history("user_123")
            # All history for session "user_123" is now cleared
        """
        if session_id in self.history:
            del self.history[session_id]

    def change_llm_type(self, model_name: str):
        """
        Changes the language model type used in the RAG pipeline.

        This method updates the LLM instance to use a different model and recreates
        the conversational chain with message history to incorporate the new model.

        Args:
            model_name (str): The name of the language model to switch to. Must be a 
                             valid model name supported by ChatGroq.

        Returns:
            None

        Raises:
            KeyError: If GROQ_API_KEY environment variable is not set.
            ValueError: If the provided model_name is not supported by ChatGroq.

        Note:
            This method reinitializes the conversational chain, so any ongoing 
            conversation context within the chain will be reset, though session 
            history will be preserved through the get_session_history method.
        """
        self.llm = ChatGroq(model_name=model_name, api_key=os.environ["GROQ_API_KEY"])
        self.chain = RunnableWithMessageHistory (
            self.ragChain,
            self.get_session_history,
            input_messages_key="Question",
            history_messages_key="History"
        )
    
    def get_llm_type(self):
        """
        Get the model name of the current language model.

        Returns:
            str: The model name of the LLM instance being used in the pipeline.
        """
        return self.llm.model_name

    def processPDF(self, pdf_path: str):
        """
        Process a PDF file by indexing it through the RAG indexing system.

        This method takes a PDF file path and processes it by calling the index_pdf
        method on the rag_indexing object to make the PDF content searchable and
        retrievable for RAG operations.

        Args:
            pdf_path (str): The file path to the PDF document to be processed.
                           Should be a valid path to an existing PDF file.

        Returns:
            None

        Raises:
            FileNotFoundError: If the PDF file at the specified path does not exist.
            ValueError: If the provided path is not a valid PDF file.
            Exception: If there are issues with the PDF indexing process.
        """
        self.rag_indexing.index_pdf(pdf_path)
