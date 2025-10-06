from Engines.BaseChatbot import BaseChatbot
from RAG.RAG_Pipeline import RAG_Pipeline

class RAG_Chatbot(BaseChatbot):
    def __init__(self, model_name="openai/gpt-oss-20b"):
        self.rag_with_history_chain = RAG_Pipeline(model_name=model_name)

    def answer(self, session_id: str, user_input: str):
        # Always yield from the pipeline's stream method
        for chunk in self.rag_with_history_chain.stream(session_id, user_input):
            yield chunk

    def getHistory(self, session_id: str) -> list[tuple[str, str]]:
        # Implement history retrieval if needed
        return self.rag_with_history_chain.get_session_history(session_id).messages

    def clearHistory(self, session_id: str) -> None:
        self.rag_with_history_chain.clear_session_history(session_id)
    
    def get_llm_type(self):
        return self.rag_with_history_chain.get_llm_type()
    
    def process_pdf(self, pdf_file) -> None:
        self.rag_with_history_chain.processPDF(pdf_file)