import sqlite3
import Student.Student as Student

class StudentDatabase:
    """
        Class for managing a student database using SQLite.
    """
    def __init__(self, db_name = 'student.db'):
        self.db_path = db_name
        self.connection = None
        self.create_table()
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def create_table(self):
        if self.connection is None:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                age INTEGER NOT NULL,
                grade VARCHAR(50) NOT NULL
            )
        ''')
        self.connection.commit()
        cursor.close()
        self.disconnect()
    
    def insertStudent(self, student):
        if self.connection is None:
            self.connect()
        if not isinstance(student, Student.Student):
            raise TypeError("Expected a Student instance")
        if not all([student.name, student.age, student.grade]):
            raise ValueError("Student attributes cannot be None")
        if not isinstance(student.age, int) or student.age <= 0:
            raise ValueError("Age must be a positive integer")
        if not isinstance(student.grade, str):
            raise ValueError("Grade must be a string")
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO students (name, age, grade) VALUES (?, ?, ?)
            ''', (student.name, student.age, student.grade))
            self.connection.commit()
            cursor.close()
            self.disconnect()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting student: {e}")
            return False
    
    def updateStudent(self, studentId, name=None, age=None, grade=None):
        if self.connection is None:
            self.connect()
        try:
            cursor = self.connection.cursor()
            query = 'UPDATE students SET '
            params = []

            if name is not None:
                query += 'name = ?, '
                params.append(name)
            if age is not None:
                query += 'age = ?, '
                params.append(age)
            if grade is not None:
                query += 'grade = ?, '
                params.append(grade)

            query = query.rstrip(', ') + ' WHERE id = ?'
            params.append(studentId)

            cursor.execute(query, tuple(params))
            self.connection.commit()
            cursor.close()
            self.disconnect()
            return True
        except sqlite3.Error as e:
            print(f"Error updating student: {e}")
            return False
    
    def deleteStudent(self, studentId):
        if( self.connection is None ):
            self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (studentId,))
            self.connection.commit()
            cursor.close()
            self.disconnect()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting student: {e}")
            return False

    def getStudent(self, studentId):
        if self.connection is None:
            self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM students WHERE id = ?', (studentId,))
            row = cursor.fetchone()
            cursor.close()
            self.disconnect()

            if row:
                return Student.Student(studentId=row[0], name=row[1], age=row[2], grade=row[3])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching student: {e}")
            return None
    
    def search_students(self, search_term):
        """Search students by name or grade"""
        if self.connection is None:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM students WHERE name LIKE ? OR grade LIKE ?"
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            records = cursor.fetchall()
            
            students = []
            for record in records:
                student = Student.Student(record[0], record[1], record[2], record[3])
                students.append(student)
            
            cursor.close()
            self.disconnect()
            return students
            
        except sqlite3.Error as e:
            print(f"Error searching students: {e}")
            return []
    
    def fetch_all_students(self):
        """
            Function to retrieve all students from the database.
        """
        if self.connection is None:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            cursor.close()
            self.disconnect()
            if not students:
                return []
            else:
                studentList = []
                for student in students:
                    studentList.append(Student.Student(studentId=student[0], name=student[1], age=student[2], grade=student[3]))
                return studentList
        except sqlite3.Error as e:
            print(f"Error fetching students: {e}")
            return []