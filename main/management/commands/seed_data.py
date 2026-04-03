from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import MuscleGroup, Exercise, Workout, WorkoutExercise


class Command(BaseCommand):
    help = "Заполняет базу начальными упражнениями, группами мышц и готовыми тренировками"

    def handle(self, *args, **kwargs):
        # -------------------- ГРУППЫ МЫШЦ --------------------
        muscle_groups_data = [
            {"name": "Грудь", "description": "Упражнения на грудные мышцы"},
            {"name": "Спина", "description": "Упражнения на мышцы спины"},
            {"name": "Ноги", "description": "Упражнения на ноги"},
            {"name": "Плечи", "description": "Упражнения на плечевой пояс"},
            {"name": "Бицепс", "description": "Упражнения на бицепс"},
            {"name": "Трицепс", "description": "Упражнения на трицепс"},
            {"name": "Пресс", "description": "Упражнения на мышцы пресса"},
        ]

        muscle_groups = {}

        for group_data in muscle_groups_data:
            group, created = MuscleGroup.objects.get_or_create(
                name=group_data["name"],
                defaults={"description": group_data["description"]}
            )
            muscle_groups[group.name] = group

            if created:
                self.stdout.write(self.style.SUCCESS(f"Создана группа мышц: {group.name}"))
            else:
                self.stdout.write(f"Уже существует группа мышц: {group.name}")

        # -------------------- УПРАЖНЕНИЯ --------------------
        exercises_data = [
            {
                "name": "Жим лёжа",
                "description": "Базовое упражнение для развития грудных мышц.",
                "difficulty": "intermediate",
                "equipment": "Штанга, скамья",
                "execution_steps": "Ляг на скамью, возьми штангу, опусти к груди и выжми вверх.",
                "muscle_groups": ["Грудь", "Трицепс"]
            },
            {
                "name": "Отжимания",
                "description": "Классическое упражнение с собственным весом.",
                "difficulty": "beginner",
                "equipment": "Без оборудования",
                "execution_steps": "Прими упор лёжа, опускайся вниз и поднимайся вверх.",
                "muscle_groups": ["Грудь", "Трицепс"]
            },
            {
                "name": "Подтягивания",
                "description": "Базовое упражнение для спины и рук.",
                "difficulty": "intermediate",
                "equipment": "Турник",
                "execution_steps": "Возьмись за перекладину и подтягивай тело вверх.",
                "muscle_groups": ["Спина", "Бицепс"]
            },
            {
                "name": "Тяга верхнего блока",
                "description": "Упражнение для широчайших мышц спины.",
                "difficulty": "beginner",
                "equipment": "Тренажёр верхнего блока",
                "execution_steps": "Тяни рукоять вниз к груди, контролируя движение.",
                "muscle_groups": ["Спина", "Бицепс"]
            },
            {
                "name": "Приседания",
                "description": "Одно из лучших базовых упражнений для ног.",
                "difficulty": "intermediate",
                "equipment": "Штанга или собственный вес",
                "execution_steps": "Поставь ноги на ширине плеч, приседай до параллели с полом и вставай.",
                "muscle_groups": ["Ноги"]
            },
            {
                "name": "Выпады",
                "description": "Упражнение для квадрицепсов и ягодиц.",
                "difficulty": "beginner",
                "equipment": "Гантели или без оборудования",
                "execution_steps": "Сделай шаг вперёд и опустись вниз до прямого угла в колене.",
                "muscle_groups": ["Ноги"]
            },
            {
                "name": "Жим гантелей сидя",
                "description": "Упражнение для развития плеч.",
                "difficulty": "intermediate",
                "equipment": "Гантели, скамья",
                "execution_steps": "Сядь, подними гантели к плечам и выжимай вверх.",
                "muscle_groups": ["Плечи"]
            },
            {
                "name": "Подъём штанги на бицепс",
                "description": "Классическое упражнение на бицепс.",
                "difficulty": "beginner",
                "equipment": "Штанга",
                "execution_steps": "Поднимай штангу к груди, не раскачивая корпус.",
                "muscle_groups": ["Бицепс"]
            },
            {
                "name": "Французский жим",
                "description": "Упражнение для трицепса.",
                "difficulty": "intermediate",
                "equipment": "Штанга или гантель",
                "execution_steps": "Опускай вес за голову и выжимай вверх.",
                "muscle_groups": ["Трицепс"]
            },
            {
                "name": "Скручивания",
                "description": "Базовое упражнение для мышц пресса.",
                "difficulty": "beginner",
                "equipment": "Без оборудования",
                "execution_steps": "Ляг на спину и поднимай корпус, напрягая пресс.",
                "muscle_groups": ["Пресс"]
            },
        ]

        created_exercises = {}

        for exercise_data in exercises_data:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data["name"],
                defaults={
                    "description": exercise_data["description"],
                    "difficulty": exercise_data["difficulty"],
                    "equipment": exercise_data["equipment"],
                    "execution_steps": exercise_data["execution_steps"],
                }
            )

            for group_name in exercise_data["muscle_groups"]:
                exercise.muscle_groups.add(muscle_groups[group_name])

            created_exercises[exercise.name] = exercise

            if created:
                self.stdout.write(self.style.SUCCESS(f"Создано упражнение: {exercise.name}"))
            else:
                self.stdout.write(f"Уже существует упражнение: {exercise.name}")

        # -------------------- ТЕХНИЧЕСКИЙ ПОЛЬЗОВАТЕЛЬ --------------------
        system_user, created = User.objects.get_or_create(
            username="system_workouts",
            defaults={
                "email": "system@example.com",
                "is_staff": False,
                "is_superuser": False,
                "is_active": False,
            }
        )

        if created:
            system_user.set_unusable_password()
            system_user.save()
            self.stdout.write(self.style.SUCCESS("Создан технический пользователь для готовых тренировок"))
        else:
            self.stdout.write("Технический пользователь уже существует")

        # -------------------- ГОТОВЫЕ ТРЕНИРОВКИ --------------------
        premade_workouts_data = [
            {
                "name": "Грудь + Трицепс",
                "description": "Базовая тренировка на грудь и трицепс",
                "exercises": [
                    {"name": "Жим лёжа", "sets": 4, "reps": "8-10", "order": 1},
                    {"name": "Отжимания", "sets": 3, "reps": "12-15", "order": 2},
                    {"name": "Французский жим", "sets": 3, "reps": "10-12", "order": 3},
                ]
            },
            {
                "name": "Спина + Бицепс",
                "description": "Тренировка на спину и бицепс",
                "exercises": [
                    {"name": "Подтягивания", "sets": 4, "reps": "6-10", "order": 1},
                    {"name": "Тяга верхнего блока", "sets": 3, "reps": "10-12", "order": 2},
                    {"name": "Подъём штанги на бицепс", "sets": 3, "reps": "10-12", "order": 3},
                ]
            },
            {
                "name": "Ноги",
                "description": "Базовая тренировка на ноги",
                "exercises": [
                    {"name": "Приседания", "sets": 4, "reps": "8-10", "order": 1},
                    {"name": "Выпады", "sets": 3, "reps": "10-12", "order": 2},
                ]
            },
            {
                "name": "Плечи",
                "description": "Базовая тренировка на плечи",
                "exercises": [
                    {"name": "Жим гантелей сидя", "sets": 4, "reps": "10-12", "order": 1},
                ]
            },
            {
                "name": "Пресс",
                "description": "Базовая тренировка на пресс",
                "exercises": [
                    {"name": "Скручивания", "sets": 4, "reps": "15-20", "order": 1},
                ]
            },
        ]

        for workout_data in premade_workouts_data:
            workout, created = Workout.objects.get_or_create(
                name=workout_data["name"],
                creator=system_user,
                defaults={
                    "description": workout_data["description"],
                    "is_premade": True,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Создана готовая тренировка: {workout.name}"))
            else:
                self.stdout.write(f"Готовая тренировка уже существует: {workout.name}")

            # Чтобы не дублировались упражнения при повторном запуске
            if workout.is_premade:
                WorkoutExercise.objects.filter(workout=workout).delete()

                for exercise_data in workout_data["exercises"]:
                    WorkoutExercise.objects.create(
                        workout=workout,
                        exercise=created_exercises[exercise_data["name"]],
                        sets=exercise_data["sets"],
                        reps=exercise_data["reps"],
                        order=exercise_data["order"],
                    )

        self.stdout.write(self.style.SUCCESS("База успешно заполнена готовыми тренировками!"))