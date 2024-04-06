import random
import copy
from metadata import *


def generate_schedule():
    schedule = [[[] for _ in range(AMOUNT_OF_DAYS)] for _ in range(AMOUNT_OF_CLASSES)]
    for i in range(AMOUNT_OF_CLASSES):
        for j in range(AMOUNT_OF_LESSONS):
            lesson = random.choice(lessons)
            if lesson[0] in classes[i].teacher.lessons:
                teacher = classes[i].teacher
            else:
                while True:
                    teacher = random.choice(teachers)
                    if lesson[0] in teacher.lessons:
                        break
            if lesson[1]:
                room = lesson[2]
            else:
                while True:
                    room = random.choice(classRooms)
                    if "cab." in room:
                        break
            day = (int)(j / MAX_AMOUNT_OF_LESSONS_PER_DAY)
            number = len(schedule[i][day])
            schedule[i][day].append(
                Lesson(classes[i], teacher, lesson[0], lesson[1], day + 1, number + 1, room))

    return schedule


def fitness(schedule):
    fitness_score = FITNESS_LIMIT

    for class_schedule in schedule:

        for day in class_schedule:
            num_lessons_per_day = len(day)
            if num_lessons_per_day > MAX_AMOUNT_OF_LESSONS_PER_DAY:
                fitness_score -= 10 * (num_lessons_per_day - MAX_AMOUNT_OF_LESSONS_PER_DAY)

        for day in class_schedule:
            for lesson in day:
                if lesson is not None:
                    if lesson.name not in lesson.teacher.lessons:
                        fitness_score -= 10

        class_teacher_lessons = 0
        for day in class_schedule:
            for lesson in day:
                if lesson is not None:
                    if lesson.cls.teacher.name == lesson.teacher.name:
                        class_teacher_lessons += 1
        if class_teacher_lessons < (AMOUNT_OF_LESSONS / 2):
            fitness_score -= 50

        window_errors = 0
        for day in class_schedule:
            lesson_amount = len(day)
            for lesson_index in range(lesson_amount):
                if day[lesson_index] is None:
                    for rest_index in range(lesson_index + 1, lesson_amount):
                        if day[rest_index] is not None:
                            window_errors += 1
        fitness_score -= 10 * window_errors

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


def mutate(schedule):
    if random.random() < MUTATION_RATE:
        for class_schedule in schedule:
            for day in class_schedule:
                for lesson in day:
                    if lesson is not None:
                        if random.random() < MUTATION_RATE and lesson is not None:
                            random_lesson = random.choice(lessons)
                            lesson.name = random_lesson[0]
                            lesson.special_room_required = random_lesson[1]
                            if random_lesson[1]:
                                lesson.room = random_lesson[2]
                            else:
                                lesson.room = random.choice(classRooms[:AMOUNT_OF_CLASSES])
                            if random_lesson[0] in lesson.cls.teacher.lessons:
                                random_teacher = lesson.cls.teacher
                            else:
                                while True:
                                    random_teacher = random.choice(teachers)
                                    if random_lesson[0] in random_teacher.lessons:
                                        break
                            lesson.teacher = random_teacher


def genetic_algorithm():
    population = [generate_schedule() for _ in range(SIZE_OF_POPULATION)]
    best_schedule = copy.deepcopy(max(population, key=lambda x: fitness(x)))
    best_fitness = fitness(best_schedule)
    for _ in range(AMOUNT_OF_GENERATIONS):
        selected_schedules = []
        for one_population in population:
            current_fitness = fitness(one_population)
            if current_fitness == FITNESS_LIMIT:
                return copy.deepcopy(one_population)
            elif best_fitness < current_fitness < FITNESS_LIMIT:
                best_schedule = copy.deepcopy(one_population)
                best_fitness = current_fitness

        child = copy.deepcopy(
            max(random.choices(population, weights=[fitness(schedule) ** 5 for schedule in population], k=10),
                key=lambda x: fitness(x)))

        mutate(child)
        selected_schedules.append(child)

        population = selected_schedules

    result_schedules = max(population, key=lambda x: fitness(x))
    if fitness(result_schedules) > best_fitness:
        best_schedule = result_schedules
    return best_schedule
