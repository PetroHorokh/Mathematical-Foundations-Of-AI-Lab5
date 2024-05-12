class Cls:
    def __init__(self, name, cls_teacher):
        self.name = name
        self.cls_teacher = cls_teacher


class Teacher:
    def __init__(self, name, lessons):
        self.name = name
        self.lessons = lessons

class Lesson:
    def __init__(self, cls="None", teacher=None, name="None", special_room_required=False,
                 day_number=0, lesson_number=0, room=""):
        self.cls = cls
        self.teacher = teacher
        self.name = name
        self.special_room_required = special_room_required
        self.day_number = day_number
        self.lesson_number = lesson_number
        self.room = room