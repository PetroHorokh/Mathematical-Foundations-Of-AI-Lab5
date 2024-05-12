from algorithm import *

def main():

    teachers = [
        Teacher("Teacher 1", ["Math", "English", "Science", "History"]),
        Teacher("Teacher 2", ["Math", "English", "Science", "Music"]),
        Teacher("Teacher 3", ["Math", "English", "Science", "History"]),
        Teacher("Teacher 4", ["PE", "Choreography"]),
    ]

    room_names = ["Room 1", "Room 2", "Room 3", "PE Room", "Dance Room", "Music Room"]

    class_names = ["Class A", "Class B", "Class C"]

    lesson_names = [["Math", False, "None"], ["English", False, "None"], ["Science", False, "None"],
                    ["History", False, "None"], ["PE", True, "PE Room"], ["Choreography", True, "Dance Room"],
                    ["Music", True, "Music Room"]]

    fileName = "input_file"
    # Запис даних у файл
    write_data_to_file(fileName, AMOUNT_OF_LESSONS, AMOUNT_OF_CLASSES, AMOUNT_OF_DAYS, MAX_AMOUNT_OF_LESSONS_PER_DAY,
                       teachers, room_names, class_names, lesson_names)

    # Читання даних з файлу
    num_lessons, num_classes, num_days, max_lessons_per_day, teachers, room_names, class_names, lesson_names = read_data_from_file(
        fileName)

    classes = []
    for i in range(num_classes):
        classes.append(ClassTeacher(class_names[i], teachers[i]))

    best_schedule = genetic_algorithm(lesson_names, teachers, classes, num_lessons, num_classes,
                                      num_days, max_lessons_per_day, room_names)

    print_schedule(best_schedule, num_days, max_lessons_per_day, num_classes, class_names)
    print(
        f"Даний розклад має пристосованість {fitness(best_schedule, num_lessons, max_lessons_per_day)} із {FITNESS_LIMIT} можливих")


if __name__ == "__main__":
    main()
