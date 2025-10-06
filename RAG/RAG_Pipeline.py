import os
from RAG.RAG_Indexing import RAG_Indexing
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

class RAG_Pipeline:
    def __init__(self, model_name=None):
        # Ensure the API key is set before constructing the default LLM
        if "GROQ_API_KEY" not in os.environ:
            os.environ["GROQ_API_KEY"] = "GROQ_API_KEY_REMOVED"
        if model_name is None:
            model_name = "Llama3-8b-8192"
        # self.llm = ChatGroq(model_name=model_name, api_key=os.environ["GROQ_API_KEY"], streaming=True)
        self.llm = ChatGroq(model_name=model_name, api_key=os.environ["GROQ_API_KEY"])
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
        if session_id not in self.history:
            self.history[session_id] = ChatMessageHistory()
        return self.history[session_id]
    
    def stream(self, session_id: str, user_input: str):
        """
        Streams the response from the RAG chain. Yields chunks if supported, otherwise returns the full response.
        Includes robust error handling.
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
        if session_id in self.history:
            del self.history[session_id]

    def change_llm_type(self, model_name: str):
        self.llm = ChatGroq(model_name=model_name, api_key=os.environ["GROQ_API_KEY"])
        self.chain = RunnableWithMessageHistory (
            self.ragChain,
            self.get_session_history,
            input_messages_key="Question",
            history_messages_key="History"
        )
    def get_llm_type(self):
        return self.llm.model_name

    def processPDF(self, pdf_path: str):
        """
        Process a PDF document by indexing its content.

        Args:
            pdf_path (str): The file path to the PDF document to be processed.
        """
        self.rag_indexing.index_pdf(pdf_path)
