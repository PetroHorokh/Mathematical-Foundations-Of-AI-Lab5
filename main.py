from algorithm import *

best_schedule = genetic_algorithm()

for i in range(AMOUNT_OF_CLASSES):

    print(f"Schedule for class {classNames[i]}\n")

    for j in range(AMOUNT_OF_DAYS):

        print(f"{days[j]}\n")

        for k in range(MAX_AMOUNT_OF_LESSONS_PER_DAY):
            lesson = best_schedule[i][j][k]

            print(f"Number: {lesson.lesson_number}")
            print(f"Subject: {lesson.name}")
            print(f"Teacher: {lesson.teacher.name}")

            print()

print(f"Result best fitness {fitness(best_schedule)} out of {FITNESS_LIMIT}")
