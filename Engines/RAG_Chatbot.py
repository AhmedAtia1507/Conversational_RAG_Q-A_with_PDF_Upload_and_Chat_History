from Engines.BaseChatbot import BaseChatbot
from RAG.RAG_Pipeline import RAG_Pipeline

class RAG_Chatbot(BaseChatbot):
    """
    A RAG (Retrieval-Augmented Generation) chatbot implementation that extends BaseChatbot.
    This class provides a conversational AI interface that combines retrieval of relevant 
    information with generative responses. It maintains chat history per session and 
    supports PDF document processing for knowledge base enhancement.
    Attributes:
        rag_with_history_chain (RAG_Pipeline): The underlying RAG pipeline that handles
            retrieval, generation, and chat history management.
    Methods:
        answer(session_id: str, user_input: str): 
            Generates streaming responses to user queries using RAG methodology.
        getHistory(session_id: str): 
            Retrieves the chat history for a specific session.
        clearHistory(session_id: str): 
            Clears the chat history for a specific session.
        get_llm_type(): 
            Returns the type of the underlying language model.
        process_pdf(pdf_file): 
            Processes and ingests PDF documents into the knowledge base.
    Example:
        >>> chatbot = RAG_Chatbot(model_name="openai/gpt-oss-20b")
        >>> chatbot.process_pdf(pdf_file)
        >>> for response in chatbot.answer("session_1", "What is the main topic?"):
        ...     print(response, end="")
    """
    def __init__(self, model_name="openai/gpt-oss-20b"):
        self.rag_with_history_chain = RAG_Pipeline(model_name=model_name)

    def answer(self, session_id: str, user_input: str):
        """
        Generates streaming responses for user queries using the RAG chatbot pipeline.

        This method processes user input through the RAG (Retrieval-Augmented Generation) 
        chain with chat history support, yielding response chunks as they are generated.

        Args:
            session_id (str): Unique identifier for the user session to maintain 
                             conversation history and context.
            user_input (str): The user's question or query to be processed by the 
                             RAG system.

        Yields:
            Any: Response chunks from the RAG pipeline as they are generated, 
                 allowing for real-time streaming of the chatbot's answer.

        Note:
            This method uses streaming to provide a responsive user experience,
            delivering partial responses as they become available rather than
            waiting for the complete response to be generated.
        """
        # Always yield from the pipeline's stream method
        for chunk in self.rag_with_history_chain.stream(session_id, user_input):
            yield chunk

    def getHistory(self, session_id: str) -> list[tuple[str, str]]:
        """
        Retrieve the chat history for a specific session.

        Args:
            session_id (str): The unique identifier for the chat session.

        Returns:
            list[tuple[str, str]]: A list of tuples containing the chat history messages,
                                  where each tuple represents a message exchange with
                                  (user_message, assistant_response) format.

        Note:
            This method retrieves the message history from the RAG chain's session
            history store. The actual implementation depends on the underlying
            history management system.
        """
        # Implement history retrieval if needed
        return self.rag_with_history_chain.get_session_history(session_id).messages

    def clearHistory(self, session_id: str) -> None:
        """
        Clear the chat history for a specific session.

        This method removes all conversation history associated with the given session ID,
        effectively resetting the chat context for that session.

        Args:
            session_id (str): The unique identifier for the session whose history should be cleared.

        Returns:
            None: This method does not return any value.

        Raises:
            None: This method does not raise any specific exceptions, though underlying
                  chain operations may raise exceptions if the session_id is invalid.
        """
        self.rag_with_history_chain.clear_session_history(session_id)
    
    def get_llm_type(self):
        """
        Get the type of the language model used in the RAG chatbot.
        
        Returns:
            str: The type/name of the language model being used by the 
                 underlying RAG chain with history.
        """
        return self.rag_with_history_chain.get_llm_type()
    
    def process_pdf(self, pdf_file) -> None:
        """
        Process a PDF file and integrate it into the RAG (Retrieval-Augmented Generation) system.

        This method takes a PDF file as input and processes it through the RAG chain with history,
        typically involving text extraction, chunking, vectorization, and storage for later retrieval
        during question-answering operations.

        Args:
            pdf_file: The PDF file to be processed. This could be a file path, file object,
                     or any format accepted by the underlying RAG processing system.

        Returns:
            None: This method doesn't return a value but modifies the internal state
                  of the RAG system by adding the processed PDF content.

        Raises:
            May raise exceptions related to PDF processing, file I/O, or vectorization
            depending on the underlying implementation of the RAG chain.
        """
        self.rag_with_history_chain.processPDF(pdf_file)