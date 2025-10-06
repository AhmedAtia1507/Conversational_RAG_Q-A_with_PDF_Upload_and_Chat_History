import logging
import os
from time import time
import streamlit as st
import json
import pandas as pd
from hashlib import sha256
from Student.Student import Student
from Student.StudentDatabase import StudentDatabase
from Engines.Legacy_Chatbot import LegacyChatbot
from Engines.RAG_Chatbot import RAG_Chatbot
from langchain_core.messages import HumanMessage, AIMessage


# Page configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
for key, default in [('logged_in', False), ('user_type', None), ('username', None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# Security functions
def hash_password(password):
    """
    Hash password using SHA-256.

    Note: This is not suitable for production-grade password storage as it does not use salt or key stretching.
    """
    return sha256(password.encode()).hexdigest()
def load_credentials():
    """Load admin credentials from JSON file"""
    try:
        with open('adminCredentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default credentials file if it doesn't exist
        default_creds = {
            "admin": {
                "username": "admin",
                "password": hash_password("admin123")
            }
        }
        with open('adminCredentials.json', 'w') as f:
            json.dump(default_creds, f, indent=4)
        return default_creds

def load_users():
    """Load user credentials from JSON file"""
    try:
        with open('userCredentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create empty users file if it doesn't exist
        with open('userCredentials.json', 'w') as f:
            json.dump({}, f)
        return {}

def save_users(users):
    """Save user credentials to JSON file"""
    with open('userCredentials.json', 'w') as f:
        json.dump(users, f, indent=4)

def authenticate_admin(username, password):
    """
    Authenticate admin credentials by comparing the provided username and
    the SHA-256 hash of the password with stored credentials.
    """
    credentials = load_credentials()
    admin_creds = credentials.get('admin', {})
    return (admin_creds.get('username') == username and 
            admin_creds.get('password') == hash_password(password))

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users = load_users()
    user_data = users.get(username, {})
    return user_data.get('password') == hash_password(password)

def register_user(username, password):
    """
    Register a new user.

    Usernames must be unique and passwords are stored as SHA-256 hashes.
    """
    users = load_users()
    if username in users:
        return False
    users[username] = {'password': hash_password(password)}
    save_users(users)
    return True

# Authentication pages
def login_page():
    """Display login page"""
    st.title("🎓 Student Database Management System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        user_type = st.radio("Login as:", ["Admin", "User"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("Login", use_container_width=True):
                if user_type == "Admin":
                    if authenticate_admin(username, password):
                        st.session_state.logged_in = True
                        st.session_state.user_type = "admin"
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid admin credentials!")
                else:
                    if authenticate_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.user_type = "user"
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid user credentials!")
        
        with col_register:
            if st.button("Register", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()

def register_page():
    """Display registration page"""
    st.title("🎓 User Registration")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Create New Account")
        
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col_reg, col_back = st.columns(2)
        
        with col_reg:
            if st.button("Register", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in all fields!")
                elif password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters!")
                elif register_user(username, password):
                    st.success("Registration successful! You can now login.")
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    st.error("Username already exists!")
        
        with col_back:
            if st.button("Back to Login", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()

# Admin dashboard
def admin_dashboard():
    """Display admin dashboard"""
    st.title(f"👨‍💼 Admin Dashboard - Welcome {st.session_state.username}!")
    
    # Initialize database
    db = StudentDatabase()
    db.create_table()
    
    # Sidebar for admin actions
    with st.sidebar:
        st.subheader("Admin Actions")
        action = st.selectbox("Choose Action", [
            "View Students",
            "Add Student",
            "Update Student",
            "Delete Student",
            "Search Students",
            "Chatbot"
        ])
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    # Main content area
    if action == "View Students":
        st.subheader("📋 All Students")
        students = db.fetch_all_students()
        
        if students:
            # Convert to DataFrame for better display
            data = []
            for student in students:
                data.append({
                    'ID': student.studentId,
                    'Name': student.name,
                    'Age': student.age,
                    'Grade': student.grade
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            
            # Download as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="students.csv",
                mime="text/csv"
            )
        else:
            st.info("No students found in the database.")
    
    elif action == "Add Student":
        st.subheader("➕ Add New Student")
        
        with st.form("add_student_form"):
            name = st.text_input("Student Name")
            age = st.number_input("Age", min_value=1, max_value=100, value=18)
            grade = st.text_input("Grade")
            
            if st.form_submit_button("Add Student"):
                if name and grade:
                    student = Student(name=name, age=age, grade=grade)
                    if db.insertStudent(student):
                        st.success(f"Student {name} added successfully!")
                    else:
                        st.error("Failed to add student!")
                else:
                    st.error("Please fill in all fields!")
    
    elif action == "Update Student":
        st.subheader("✏️ Update Student")
        
        students = db.fetch_all_students()
        if students:
            # Select student to update
            student_options = {f"{s.name} (ID: {s.studentId})": s.studentId for s in students}
            selected_student = st.selectbox("Select Student", list(student_options.keys()))
            
            if selected_student:
                studentId = student_options[selected_student]
                student = db.getStudent(studentId)
                
                if student:
                    with st.form("update_student_form"):
                        name = st.text_input("Name", value=student.name)
                        age = st.number_input("Age", min_value=1, max_value=100, value=student.age)
                        grade = st.text_input("Grade", value=student.grade)
                        
                        if st.form_submit_button("Update Student"):
                            if db.updateStudent(studentId, name, age, grade):
                                st.success("Student updated successfully!")
                            else:
                                st.error("Failed to update student!")
        else:
            st.info("No students found to update.")
    
    elif action == "Delete Student":
        st.subheader("🗑️ Delete Student")
        
        students = db.fetch_all_students()
        if students:
            student_options = {f"{s.name} (ID: {s.studentId})": s.studentId for s in students}
            selected_student = st.selectbox("Select Student to Delete", list(student_options.keys()))
            
            if selected_student:
                studentId = student_options[selected_student]
                
                st.warning(f"Are you sure you want to delete {selected_student}?")
                if st.button("Delete Student", type="primary"):
                    if db.delete_student(studentId):
                        st.success("Student deleted successfully!")
                    else:
                        st.error("Failed to delete student!")
        else:
            st.info("No students found to delete.")
        
    elif action == "Search Students":
        st.subheader("🔍 Search Students")
        
        search_term = st.text_input("Search by name or grade")
        
        if search_term:
            students = db.search_students(search_term)
            
            if students:
                data = []
                for student in students:
                    data.append({
                        'ID': student.studentId,
                        'Name': student.name,
                        'Age': student.age,
                        'Grade': student.grade
                    })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info(f"No students found matching '{search_term}'")
    
    elif action == "Chatbot":
        chatbot_interface()

# User dashboard
def user_dashboard():
    """Display user dashboard"""
    st.title(f"👤 User Dashboard - Welcome {st.session_state.username}!")
    
    with st.sidebar:
        st.subheader("User Menu")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    chatbot_interface()

# Chatbot interface
def chatbot_interface():
    """Display chatbot interface"""
    st.subheader("🤖 Student Information Chatbot")
    
    with st.sidebar:
        st.subheader("Chatbot Settings")
        engine_type = st.selectbox(
            "Select Engine", 
            ["Legacy Chatbot", "RAG Chatbot"],
            index=0
        )
        # Session ID management: allow user to select or add session IDs
        if "session_ids" not in st.session_state:
            st.session_state.session_ids = []

        st.markdown("**Session Management**")
        session_ids = st.session_state.session_ids

        # Add new session ID
        new_session_id = st.text_input("Add new Session ID", value="", placeholder="Enter new session ID")
        if st.button("Add Session ID"):
            if new_session_id.strip() != "" and new_session_id not in session_ids:
                session_ids.append(new_session_id.strip())
                st.session_state.session_ids = session_ids
                st.success(f"Session ID '{new_session_id.strip()}' added.")
            elif new_session_id.strip() in session_ids:
                st.warning("Session ID already exists.")
            else:
                st.warning("Please enter a valid session ID.")

        # Select session ID from list
        if session_ids:
            session_id = st.selectbox("Select Session ID", session_ids)
        else:
            st.info("No session IDs available. Please add one to start chatting.")
            return

        # Optionally allow user to remove a session ID
        remove_session_id = st.selectbox("Remove Session ID", [""] + session_ids)
        if remove_session_id and remove_session_id != "":
            if st.button("Remove Selected Session ID"):
                session_ids.remove(remove_session_id)
                st.session_state.session_ids = session_ids
                st.success(f"Session ID '{remove_session_id}' removed.")
                st.rerun()
    
    if session_id and session_id != st.session_state.get("current_session_id"):
        st.session_state.current_session_id = session_id
    model_choice = None
    groq_api_key = None
    uploaded_file = None

    # Sidebar for RAG settings
    if engine_type == "RAG Chatbot":
        with st.sidebar:
            groq_api_key = st.text_input(
                "Groq API Key",
                value="",
                type="password",
                help="Enter your Groq API key from console.groq.com",
                placeholder="gsk_..."
            )
            model_choice = st.selectbox(
                "Choose Groq Model:",
                [
                    "openai/gpt-oss-20b",
                    "llama-3.3-70b-versatile",
                    "mistral-saba-24b",
                    "gemma2-9b-it"
                ],
                index=0,
                help="Select which Groq model to use for summarization"
            )
            model_info = {
                "openai/gpt-oss-20b": "OpenAI GPT-OSS 20B - Powerful language model",
                "llama-3.3-70b-versatile": "Meta Llama 3.3 70B - Most capable (replaces llama3-70b-8192)",
                "mistral-saba-24b": "Mistral Saba 24B - Good balance of speed and quality (replaces mixtral-8x7b-32768)",
                "gemma2-9b-it": "Google Gemma 2 9B - Latest version"
            }
            if model_choice in model_info:
                st.info(f"ℹ️ {model_info[model_choice]}")
            if groq_api_key.strip() == "":
                st.warning("Please enter your Groq API key to use the RAG Chatbot.")
                return
            else:
                os.environ["GROQ_API_KEY"] = groq_api_key.strip()
            uploaded_file = st.file_uploader("Upload PDF", type="pdf")
            if uploaded_file:
                st.success(f"Uploaded file: {uploaded_file}")

    # Store chatbot in session_state
    chatbot_key = f"chatbot_{engine_type}_{model_choice if model_choice else ''}"
    if "chatbot_key" not in st.session_state or st.session_state.get("chatbot_key") != chatbot_key:
        st.session_state["chatbot_key"] = chatbot_key
        if engine_type == "Legacy Chatbot":
            st.session_state.chatbot = LegacyChatbot()
        elif engine_type == "RAG Chatbot":
            st.session_state.chatbot = RAG_Chatbot(model_name=model_choice)

    # PDF upload handling for RAG
    if engine_type == "RAG Chatbot" and uploaded_file is not None:
        try:
            file_bytes = uploaded_file.read()
            file_size_mb = len(file_bytes) / (1024 * 1024)
            if file_size_mb > 10:
                st.error("PDF is too large (max 10MB). Please upload a smaller file.")
            else:
                with st.spinner("Processing PDF and embedding... This may take a moment."):
                    st.session_state.chatbot.process_pdf(file_bytes)
        except Exception as e:
            st.error(f"Error processing PDF: {e}")


    chat_container = st.container()
    with chat_container:
        history = st.session_state.chatbot.getHistory(session_id)
        if not history:
            st.markdown("No chat history found.")
        else:
            for i, msg in enumerate(history):
                if isinstance(msg, HumanMessage):
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(msg.content)
                if isinstance(msg, AIMessage):
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(msg.content)
                st.markdown("---")

    def send_message(user_input):
        if user_input.strip():
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)
            if isinstance(st.session_state.chatbot, LegacyChatbot):
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(st.session_state.chatbot.answer(st.session_state.current_session_id, user_input))
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Generating answer..."):
                        st.write_stream(st.session_state.chatbot.answer(st.session_state.current_session_id, user_input))

    user_input = st.chat_input("Ask me:", key="chat_input")
    if user_input:
        send_message(user_input)

    if st.button("Clear Chat"):
        st.session_state.chatbot.clearHistory(session_id)

# Main application logic
def main():
    """Main application function"""
    # Check if user wants to register
    if 'show_register' in st.session_state and st.session_state.show_register:
        register_page()
    elif not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_type == "admin":
            admin_dashboard()
        else:
            user_dashboard()

if __name__ == "__main__":
    main()