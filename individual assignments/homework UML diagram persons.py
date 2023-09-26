from msilib.schema import tables
from random import randint

class Person:
    def __init__(self, age, name, height, eyeColour):
        self.age=age
        self.name=name
        self.height=height
        self.eyeColour=eyeColour
        print("person is created")

    def speak(self):
        print("*people noises*")
        return 0

    def learn(self):
        print("hmmmmm learning right now man")
        return 0

    def whoIsThis(self):
        return f"I am a {self.__class__.__name__}, I am {self.age} years old. " \
            f"My name is {self.name} and I have {self.eyeColour} eyes. My height = {self.height}cm"


class Student(Person):
    def __init__(self, number, course, name, age, height, eyeColour, password):
        super().__init__(name, age, height, eyeColour)
        self.student_number = number
        self.course = course
        self.password = password
    
    @property
    def password(self):
            return self._password


    @password.setter
    def password(self, text):
        try:
            self._password = str(text)
            print("Accepted")
        except ValueError:
            raise ValueError('"password" must be float') from None
    

    def doExams():
        score = randint(0,100)
        print(f"Final exam result is {score}")

    def doHomework():
        print("I'm doing homework")


class Teacher(Person):
    
    #instance attributes
    def __init__(self, name,height,eyeColour, age, teacher_abv, degree):
        super().__init__(age, name, height, eyeColour)
        self.teacher_abv = teacher_abv
        self.degree = degree


     #instance methods
    def grade(self):
        return f"{self.name} is grading"

    def berate(self):
        return f"{self.name} is berating"


John=Student(788799, "Mechatronics", "John", 20, 180, "blue", 10)

