import random
import copy
import tkinter as tk
from tkinter import ttk
from constans import *
from classes import *
from input import *

# Генерація випадкового розкладу
def generate_schedule(lesson_names, teachers, classes, num_lessons, num_classes, num_days,
                      max_lessons_per_day, room_names):
    schedule = []
    for i in range(num_classes):
        schedule.append([])
        for j in range(num_days):
            schedule[i].append([])
    for i in range(num_classes):
        for j in range(num_lessons):
            random_lesson = random.choice(lesson_names)
            if random_lesson[0] in classes[i].cls_teacher.lessons:
                random_teacher = classes[i].cls_teacher
            else:
                while True:
                    random_teacher = random.choice(teachers)
                    if random_lesson[0] in random_teacher.lessons:
                        break
            if random_lesson[1]:
                random_room = random_lesson[2]
            else:
                random_room = random.choice(room_names[:num_classes])
            day_number = j % max_lessons_per_day
            lesson_number = len(schedule[i][day_number])
            schedule[i][day_number].append(Lesson(classes[i], random_teacher, random_lesson[0],
                                                  random_lesson[1], day_number + 1, lesson_number + 1, random_room))
    for i in range(num_classes):
        for j in range(num_days * max_lessons_per_day - num_lessons):
            day_number = j % max_lessons_per_day
            schedule[i][day_number].append(None)

    return schedule


def fitness(schedule, num_lessons, max_lessons_per_day):
    fitness_score = max_fitness

    for class_schedule in schedule:

        # Перевірка кількості уроків на день
        for day in class_schedule:
            num_lessons_per_day = len(day)
            if num_lessons_per_day > max_lessons_per_day:
                fitness_score -= 10 * (num_lessons_per_day - max_lessons_per_day)

        # Перевірка вчитель відповідає предмету
        for day in class_schedule:
            for lesson in day:
                if lesson is not None:
                    if lesson.name not in lesson.teacher.lessons:
                        fitness_score -= 10

        # Перевірка класний керівник веде хоча б половину предметів
        class_teacher_lessons = 0
        for day in class_schedule:
            for lesson in day:
                if lesson is not None:
                    if lesson.cls.cls_teacher.name == lesson.teacher.name:
                        class_teacher_lessons += 1
        if class_teacher_lessons < (num_lessons / 2):
            fitness_score -= 50

        # Перевірка вікно у розкладі
        window_errors = 0
        for day in class_schedule:
            lesson_amount = len(day)
            for lesson_index in range(lesson_amount):
                if day[lesson_index] is None:
                    for rest_index in range(lesson_index + 1, lesson_amount):
                        if day[rest_index] is not None:
                            window_errors += 1
        fitness_score -= 10 * window_errors

    # Перевірка вчитель веде 2 уроки одночасно та однакові кімнати зайняті одночасно
    same_teacher_errors = 0
    same_room_errors = 0
    all_lessons = []
    for class_schedule in schedule:
        for day in class_schedule:
            for lesson in day:
                all_lessons.append(lesson)
    for lesson_index in range(len(all_lessons)):
        for another_lesson_index in range(lesson_index + 1, len(all_lessons)):
            first_lesson = all_lessons[lesson_index]
            second_lesson = all_lessons[another_lesson_index]
            if first_lesson is not None and second_lesson is not None:
                if (first_lesson.day_number == second_lesson.day_number) and \
                        (first_lesson.lesson_number == second_lesson.lesson_number) and \
                        (first_lesson.teacher.name == second_lesson.teacher.name):
                    same_teacher_errors += 1
                if (first_lesson.day_number == second_lesson.day_number) and \
                        (first_lesson.lesson_number == second_lesson.lesson_number) and \
                        (first_lesson.room == second_lesson.room):
                    same_room_errors += 1
    fitness_score -= 10 * same_teacher_errors
    fitness_score -= 10 * same_room_errors

    return fitness_score


def mutate(schedule, lesson_names, teachers, room_names, num_classes):
    if random.random() < mutation_rate:
        for class_schedule in schedule:
            for day in class_schedule:
                for lesson in day:
                    if lesson is not None:
                        if random.random() < mutation_rate and lesson is not None:
                            random_lesson = random.choice(lesson_names)
                            lesson.name = random_lesson[0]
                            lesson.special_room_required = random_lesson[1]
                            if random_lesson[1]:
                                lesson.room = random_lesson[2]
                            else:
                                lesson.room = random.choice(room_names[:num_classes])
                            if random_lesson[0] in lesson.cls.cls_teacher.lessons:
                                random_teacher = lesson.cls.cls_teacher
                            else:
                                while True:
                                    random_teacher = random.choice(teachers)
                                    if random_lesson[0] in random_teacher.lessons:
                                        break
                            lesson.teacher = random_teacher


def crossover(parent1_schedule, parent2_schedule, num_lessons, num_classes, num_days, max_lessons_per_day):
    child_schedule = []
    for i in range(num_lessons):
        child_schedule.append([])
        for j in range(num_days):
            child_schedule[i].append([])
    for i in range(num_classes):
        for j in range(num_days):
            crossover_class_point = random.randint(0, max_lessons_per_day - 1)
            child_schedule[i][j] = \
                parent1_schedule[i][j][:crossover_class_point] + parent2_schedule[i][j][crossover_class_point:]

    return child_schedule


def genetic_algorithm(lesson_names, teachers, classes, num_lessons, num_classes,
                      num_days, max_lessons_per_day, room_names):
    population = [generate_schedule(lesson_names, teachers, classes, num_lessons, num_classes,
                                    num_days, max_lessons_per_day, room_names) for _ in range(population_size)]
    best_schedule = copy.deepcopy(max(population, key=lambda x: fitness(x, num_lessons, max_lessons_per_day)))
    best_fitness = fitness(best_schedule, num_lessons, max_lessons_per_day)

    for generation in range(max_generations):
        fitness_scores = [fitness(schedule, num_lessons, max_lessons_per_day) ** 5 for schedule in population]
        selected_schedules = []

        for one_population in population:

            current_fitness = fitness(one_population, num_lessons, max_lessons_per_day)
            if current_fitness == max_fitness:
                return copy.deepcopy(one_population)
            elif fitness(one_population, num_lessons, max_lessons_per_day) > best_fitness:
                best_schedule = copy.deepcopy(one_population)
                best_fitness = fitness(best_schedule, num_lessons, max_lessons_per_day)

            # Турнірна вибірка
            new_children = random.choices(population, weights=fitness_scores, k=10)
            child = copy.deepcopy(max(new_children, key=lambda x: fitness(x, num_lessons, max_lessons_per_day)))

            # Схрещування
            # parent1 = random.choices(population, weights=fitness_scores)[0]
            # parent2 = random.choices(population, weights=fitness_scores)[0]
            # if random.random() < crossover_rate:
            #     child = copy.deepcopy(crossover(parent1, parent2, num_lessons,
            #                                     num_classes, num_days, max_lessons_per_day))
            # else:
            #     child = copy.deepcopy(max([parent1, parent2],
            #                               key=lambda x: fitness(x, num_lessons, max_lessons_per_day)))

            mutate(child, lesson_names, teachers, room_names, num_classes)
            selected_schedules.append(child)

        population = selected_schedules

    result_schedules = max(population, key=lambda x: fitness(x, num_lessons, max_lessons_per_day))
    if fitness(result_schedules, num_lessons, max_lessons_per_day) > best_fitness:
        best_schedule = result_schedules
    return best_schedule


def print_schedule(schedule, num_days, max_lessons_per_day, num_classes, class_names):
    # Створення головного вікна
    root = tk.Tk()
    root.title("Schedule")
    root.geometry("800x600")  # Розмір вікна

    # Встановлення стилю з ttkthemes
    style = ttk.Style()
    style.configure("Treeview", rowheight=52, borderwidth=3,
                    relief="solid", color = 'black')  # Збільшення висоти рядків та задання рамки

    # Створення таблиці
    table = ttk.Treeview(root, columns=["Day", "Lesson Number"] + class_names[:num_classes], show="headings",
                         height=num_days * max_lessons_per_day * 2, style="Treeview")  # Збільшення висоти рядка
    table.heading("Day", text="Day")
    table.heading("Lesson Number", text="Lesson Number")
    for class_name in class_names[:num_classes]:
        table.heading(class_name, text=class_name)

    for day_index in range(num_days):
        for lesson_index in range(max_lessons_per_day):
            row_data = []
            for class_index in range(num_classes):
                if lesson_index >= len(schedule[0][day_index]):
                    row_data.append(" ")
                else:
                    lesson = schedule[class_index][day_index][lesson_index]
                    row_data.append(f"{lesson.name}\n{lesson.teacher.name}\n{lesson.room}")

            if lesson_index == 0:
                table.insert("", tk.END, values=[f"Day {day_index + 1}", f"Lesson {lesson_index + 1}"] + row_data)
            else:
                table.insert("", tk.END, values=["", f"Lesson {lesson_index + 1}"] + row_data)

        if day_index < num_days - 1:
            table.insert("", tk.END, values=[""] * (num_classes + 2))

    # Відображення таблиці з використанням прокрутки
    scroll_y = ttk.Scrollbar(root, orient="vertical", command=table.yview)
    table.configure(yscroll=scroll_y.set)
    table.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Запуск головного циклу вікна
    root.mainloop()

def main():
    num_lessons = 23
    num_classes = 2
    num_days = 5
    max_lessons_per_day = 5

    teachers = [
        Teacher("Вчитель 1", ["Математика", "Англійська", "Наука", "Історія"]),
        Teacher("Вчитель 2", ["Математика", "Англійська", "Наука", "Музика"]),
        Teacher("Вчитель 3", ["Математика", "Англійська", "Наука", "Історія"]),
        Teacher("Вчитель 4", ["Фізичне виховання", "Хореографія"]),
    ]

    room_names = ["Клас 1", "Клас 2", "Клас 3", "Спортзал", "Хореографічний кабінет", "Музична кімната"]

    class_names = ["Клас A", "Клас B", "Клас C"]

    lesson_names = [["Математика", False, "None"], ["Англійська", False, "None"], ["Наука", False, "None"],
                    ["Історія", False, "None"], ["Фізичне виховання", True, "Спортзал"], ["Хореографія", True, "Хореографічний кабінет"],
                    ["Музика", True, "Музична кімната"]]

    # fileName = "save"
    # # Запис даних у файл
    # write_data_to_file(fileName, num_lessons, num_classes, num_days, max_lessons_per_day,
    #                    teachers, room_names, class_names, lesson_names)
    #
    # # Читання даних з файлу
    # num_lessons, num_classes, num_days, max_lessons_per_day, teachers, room_names, class_names, lesson_names = read_data_from_file(
    #     fileName)

    classes = []
    for i in range(num_classes):
        classes.append(Cls(class_names[i], teachers[i]))

    best_schedule = genetic_algorithm(lesson_names, teachers, classes, num_lessons, num_classes,
                                      num_days, max_lessons_per_day, room_names)

    for class_schedule in best_schedule:
        class_teacher_lessons = 0
        number_of_lessons = 0
        class_name = ''
        for day in class_schedule:
            for lesson in day:
                if lesson is not None:
                    number_of_lessons += 1
                    class_name = lesson.cls.name
                    if lesson.cls.cls_teacher.name == lesson.teacher.name:
                        class_teacher_lessons += 1
        print(f'У класі {class_name} класний керівник веде {class_teacher_lessons / number_of_lessons}% уроків')

    print_schedule(best_schedule, num_days, max_lessons_per_day, num_classes, class_names)
    print(
        f"Даний розклад має пристосованість {fitness(best_schedule, num_lessons, max_lessons_per_day)} із {max_fitness} можливих")


if __name__ == "__main__":
    main()
