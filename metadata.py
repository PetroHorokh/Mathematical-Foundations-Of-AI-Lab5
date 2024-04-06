from classes import *
from constans import *

teachers = [
    Teacher("Teacher №1", ["Math", "Ukrainian", "Science", "History"]),
    Teacher("Teacher №2", ["History", "English", "Science", "Music"]),
    Teacher("Teacher №3", ["Literature", "Ukrainian", "Science", "Ethics"]),
    Teacher("Teacher №4", ["PE", "Choreography"]),
]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

classRooms = ["cab. 101", "cab. 102", "cab. 103", "cab. 104", "PE space", "Dance space", "Music space", "Physics space"]

lessons = [
    ["Math", False, "None"],
    ["English", False, "None"],
    ["Ukrainian", False, "None"],
    ["Science", False, "None"],
    ["History", False, "None"],
    ["Literature", False, "None"],
    ["Ethics", False, "None"],
    ["PE", True, "PE Room"],
    ["Choreography", True, "Dance Room"],
    ["Music", True, "Music Room"]]

classNames = ["A", "B", "C"]

classes = [ClassTeacher(classNames[i], teachers[i]) for i in range(AMOUNT_OF_CLASSES)]
