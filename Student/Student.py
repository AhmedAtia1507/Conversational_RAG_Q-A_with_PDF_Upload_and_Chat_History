class Student:
    """
        - Class representing a student with attributes such as studentId, name, age, and grade.
        - It includes methods for updating student information, converting to a dictionary, and string representation.
    """
    def __init__(self, studentId = None, name = None, age = None, grade = None):
        self.studentId = studentId
        self.name = name
        self.age = age
        self.grade = grade
    
    def __str__(self):
        return f"Student Name: {self.name}, Student Age: {self.age}, Student Grade: {self.grade}"

    def __repr__(self):
        return f"Student({self.studentId}, {self.name}, {self.age}, {self.grade})"
    
    def update(self, studentId=None, name=None, age=None, grade=None):
        if studentId is not None:
            self.studentId = studentId
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if grade is not None:
            self.grade = grade
    
    def to_dict(self):
        return {
            "studentId": self.studentId,
            "name": self.name,
            "age": self.age,
            "grade": self.grade
        }
    