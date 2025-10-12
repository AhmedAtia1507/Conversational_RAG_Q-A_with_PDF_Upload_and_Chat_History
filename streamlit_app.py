import streamlit as st
from Engines.RAG_Chatbot import RAG_Chatbot
from langchain_core.messages import HumanMessage, AIMessage
import logging
import os

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatApp:
    def __init__(self):
        self.set_page_config()
        self.initialize_session_state()
        
    def initialize_session_state(self):
        if 'thread_ids' not in st.session_state:
            st.session_state.thread_ids = ["Default Thread"]
            st.session_state.current_thread_id = "Default Thread"
        
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []

    def set_page_config(self):
        st.set_page_config(
            page_title="Conversational RAG Chatbot",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def display_sidebar(self):
        with st.sidebar:
            st.title("🤖 RAG Chatbot Settings")

            st.session_state.selected_model = st.selectbox (
                "Select Language Model",
                options=[
                    "openai/gpt-oss-120b",
                    "openai/gpt-oss-20b",
                    "llama-3.3-70b-versatile",
                    "gemma2-9b-it"
                ],
                index=0
            )

            st.session_state.api_key = st.text_input("Enter your Groq API Key:", type="password")

            if st.session_state.api_key and st.session_state.selected_model:
                os.environ["GROQ_API_KEY"] = st.session_state.api_key
                st.success("API Key and Model selected!")
                if 'chatbot' not in st.session_state or st.session_state.chatbot.get_llm_type() != st.session_state.selected_model:
                    with st.spinner("Initializing chatbot..."):
                        st.session_state.chatbot = RAG_Chatbot(st.session_state.selected_model)
                        st.success("Chatbot initialized!")
            st.markdown("---")

            st.session_state.current_thread_id = st.selectbox(
                "Select Chat Thread",
                options=st.session_state.thread_ids if st.session_state.thread_ids else ["Default Thread"],
                index=st.session_state.thread_ids.index(st.session_state.current_thread_id) if st.session_state.current_thread_id in st.session_state.thread_ids else 0
            )

            if st.button("Create New Thread"):
                new_thread_id = f"Thread {len(st.session_state.thread_ids) + 1}"
                st.session_state.thread_ids.append(new_thread_id)
                st.session_state.current_thread_id = new_thread_id
                st.success(f"Created and switched to {new_thread_id}")

            st.markdown("---")

            uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

            if uploaded_file is not None and 'chatbot' in st.session_state and uploaded_file.file_id not in st.session_state.uploaded_files:
                st.session_state.uploaded_files.append(uploaded_file.file_id)
                with st.spinner("Processing PDF and embedding..."):
                    st.session_state.chatbot.process_pdf(uploaded_file)
                    st.success("PDF processed and embedded successfully!")
        
    def display_chat_messages(self):
        if 'chatbot' not in st.session_state:
            return
        messages = st.session_state.chatbot.getHistory(st.session_state.current_thread_id)
        for _, message in enumerate(messages):
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)
    
    def handle_user_input(self, prompt):
        if 'chatbot' not in st.session_state:
            st.error("Chatbot not initialized. Please enter the Groq API key in the sidebar.")
            return
        try:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Processing your request..."):
                    st.write_stream(st.session_state.chatbot.answer(st.session_state.current_thread_id, prompt))
        except Exception as e:
            logging.error(f"Error handling user input: {e}")
            st.error(f"An error occurred: {e}")

    def display_chat_interface(self):
        self.display_chat_messages()

        if prompt := st.chat_input("Ask a question about your documents..."):
            self.handle_user_input(prompt)
    
    def run(self):
        try:
            st.title("🤖 Conversational RAG Chatbot with PDF Upload and Chat History")
            self.display_sidebar()

            if 'chatbot' not in st.session_state:
                st.error("Please enter your Groq API key in the sidebar to initialize the chatbot.")
                st.stop()
            
            self.display_chat_interface()
        except Exception as e:
            logging.error(f"Error running chat app: {e}")
            st.error(f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    app = ChatApp()
    app.run()