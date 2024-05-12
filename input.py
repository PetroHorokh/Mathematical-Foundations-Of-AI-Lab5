from classes import *

def write_data_to_file(filename, num_lessons, num_classes, num_days, max_lessons_per_day,
                       teachers, room_names, class_names, lesson_names):
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(f"{num_lessons}\n")
        file.write(f"{num_classes}\n")
        file.write(f"{num_days}\n")
        file.write(f"{max_lessons_per_day}\n")

        for teacher in teachers:
            lessons_str = ", ".join(teacher.lessons)
            file.write(f"{teacher.name}: {lessons_str}\n")

        for room_name in room_names:
            file.write(f"{room_name}\n")

        for class_name in class_names:
            file.write(f"{class_name}\n")

        for lesson_name in lesson_names:
            requires_room = str(lesson_name[1]).lower()
            room_name = lesson_name[2]
            file.write(f"{lesson_name[0]}, {requires_room}, {room_name}\n")


def read_data_from_file(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    num_lessons = int(lines[0].strip())
    num_classes = int(lines[1].strip())
    num_days = int(lines[2].strip())
    max_lessons_per_day = int(lines[3].strip())

    teachers = []
    for line in lines[4:8]:
        name, lessons_str = line.split(":")
        lessons = [lesson.strip() for lesson in lessons_str.split(",")]
        teachers.append(Teacher(name.strip(), lessons))

    room_names = [name.strip() for name in lines[8:14]]
    class_names = [name.strip() for name in lines[14:14 + num_classes]]

    lesson_names = []
    for line in lines[14 + num_classes:14 + num_classes + num_lessons]:
        values = line.split(",")
        if len(values) == 3:
            name, requires_room_str, room_name = values
            requires_room = requires_room_str.strip().lower() == "true"
            room_name = room_name.strip() if requires_room else "None"
            lesson_names.append([name.strip(), requires_room, room_name])

    return num_lessons, num_classes, num_days, max_lessons_per_day, teachers, room_names, class_names, lesson_names