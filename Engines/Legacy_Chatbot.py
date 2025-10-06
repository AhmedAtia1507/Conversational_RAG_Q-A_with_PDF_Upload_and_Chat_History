from Student.StudentDatabase import StudentDatabase
from Engines.BaseChatbot import BaseChatbot
from langchain_core.messages import HumanMessage, AIMessage
import re

class LegacyChatbot(BaseChatbot):
    """
    LegacyChatbot provides a conversational interface for querying student information from a database.
    Features:
    - Handles greetings, farewells, and help requests.
    - Answers queries about student count, average age, and lists all students.
    - Supports searching for students by name or grade.
    - Finds the oldest and youngest students.
    - Maintains chat history per session.
    Methods:
        __init__(): Initializes the chatbot, student database, response templates, and chat history.
        answer(session_id, user_input): Processes user input and returns an appropriate response, updating chat history.
        getHistory(session_id): Retrieves chat history for a given session.
        process_query(user_input): Interprets user queries and routes them to the correct handler.
        get_student_count(): Returns the total number of students in the database.
        get_average_age(): Calculates and returns the average age of students.
        search_student_by_name(name): Searches for students by name and returns matching results.
        get_students_by_grade(grade): Returns all students in a specified grade.
        list_all_students(): Lists all students in the database.
        get_oldest_student(): Finds and returns the oldest student.
        get_youngest_student(): Finds and returns the youngest student.
        default_response(user_input): Provides a default response for unrecognized queries.
    """

    def __init__(self):
        self.db = StudentDatabase()
        self.responses = {
            'greeting': [
                "Hello! I'm here to help you with student information. What would you like to know?"
            ],
            'goodbye': [
                "Goodbye! Feel free to ask me anything anytime!"
            ],
            'help': [
                "I can help you with:\n- Finding student information\n- Getting student count\n- Searching by name or grade\n- Average age calculations\n\nJust ask me naturally!"
            ]
        }
        self.history = {}

    def answer(self, session_id, user_input):
        """Process user query and return appropriate response"""
        user_input = user_input.lower().strip()
        response = self.process_query(user_input)
        self.history[session_id] = self.history.get(session_id, [])
        self.history[session_id].append(HumanMessage(content=user_input))
        self.history[session_id].append(AIMessage(content=response))
        return response
    
    def getHistory(self, session_id):
        """Retrieve chat history for a given session"""
        return self.history.get(session_id, [])
    
    def clearHistory(self, session_id):
        """Clear chat history for a given session"""
        if session_id in self.history:
            del self.history[session_id]

    def process_query(self, user_input):
        # Greeting patterns
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
            return self.responses['greeting'][0]
        
        # Goodbye patterns
        if any(word in user_input for word in ['bye', 'goodbye', 'see you', 'exit']):
            return self.responses['goodbye'][0]
        
        # Help patterns
        if any(word in user_input for word in ['help', 'what can you do', 'commands']):
            return self.responses['help'][0]
        
        # Student count queries
        if 'how many students' in user_input or 'total students' in user_input or 'count' in user_input:
            return self.get_student_count()
        
        # Average age queries
        if 'average age' in user_input or 'mean age' in user_input:
            return self.get_average_age()
        
        # Search by name
        if 'find student' in user_input or 'search for' in user_input:
            # Extract name from query
            name_match = re.search(r'(?:find student|search for)\s+(.+)', user_input)
            if name_match:
                name = name_match.group(1)
                return self.search_student_by_name(name)
        
        # Search by grade
        if re.search(r'(students (in|with|of)? grade\s+\w+|show students in grade\s+\w+)', user_input):
            grade_match = re.search(r'grade\s+(\w+)', user_input)
            if grade_match:
                grade = grade_match.group(1)
                return self.get_students_by_grade(grade)
        
        # List all students
        if 'list all students' in user_input or 'show all students' in user_input or 'all students' in user_input:
            return self.list_all_students()
        
        # Oldest/youngest student
        if 'oldest student' in user_input:
            return self.get_oldest_student()
        
        if 'youngest student' in user_input:
            return self.get_youngest_student()
        
        # Default response for unrecognized queries
        return self.default_response(user_input)
    
    def get_student_count(self):
        """Get total number of students"""
        students = self.db.fetch_all_students()
        count = len(students)
        if count == 0:
            return "There are currently no students in the database."
        elif count == 1:
            return "There is currently 1 student in the database."
        else:
            return f"There are currently {count} students in the database."
    
    def get_average_age(self):
        """Calculate and return average age of students"""
        students = self.db.fetch_all_students()
        if not students:
            return "No students found to calculate average age."
        
        total_age = sum(student.age for student in students)
        average_age = total_age / len(students)
        return f"The average age of students is {average_age:.1f} years."
    
    def search_student_by_name(self, name):
        """Search for student by name"""
        students = self.db.search_students(name)
        if not students:
            return f"No student found with the name '{name}'."
        
        if len(students) == 1:
            student = students[0]
            return "Found student: " + student.__str__()
        else:
            result = f"Found {len(students)} students matching '{name}':\n"
            for student in students:
                result += "- " + student.__str__() + "\n"
            return result
    
    def get_students_by_grade(self, grade):
        """Get all students in a specific grade"""
        students = self.db.search_students(grade)
        if not students:
            return f"No students found with grade {grade}."
        
        result = f"Students with grade {grade}:\n"
        for student in students:
            result += f"- {student.name}, Age: {student.age}\n"
        return result
    
    def list_all_students(self):
        """List all students in the database"""
        students = self.db.fetch_all_students()
        if not students:
            return "No students found in the database."
        
        result = "All students in the database:\n"
        for student in students:
            result += f"- " + student.__str__() + "\n"
        return result
    
    def get_oldest_student(self):
        """Find the oldest student"""
        students = self.db.fetch_all_students()
        if not students:
            return "No students found in the database."
        
        oldest = max(students, key=lambda s: s.age)
        return f"The oldest student is {oldest.name}, age {oldest.age}, with grade {oldest.grade}."
    
    def get_youngest_student(self):
        """Find the youngest student"""
        students = self.db.fetch_all_students()
        if not students:
            return "No students found in the database."
        
        youngest = min(students, key=lambda s: s.age)
        return f"The youngest student is {youngest.name}, age {youngest.age}, with grade {youngest.grade}."
    
    def default_response(self, user_input):
        """Default response for unrecognized queries"""
        return f"I'm not sure how to help with '{user_input}'. Try asking about:\n" \
               "- Student count ('How many students are there?')\n" \
               "- Average age ('What's the average age?')\n" \
               "- Finding students ('Find student John')\n" \
               "- Students by grade ('Students with grade Excellent')\n" \
               "- List all students ('Show all students')\n" \
               "- Oldest/youngest student"