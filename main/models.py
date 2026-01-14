from django.db import models

# Create your models here.

class TempUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.username
class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название группы мышц")
    description = models.TextField(blank=True, verbose_name="Описание")
    # Можно добавить изображение: icon = models.ImageField(upload_to='muscle_icons/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа мышц"
        verbose_name_plural = "Группы мышц"


class Exercise(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название упражнения")
    description = models.TextField(verbose_name="Подробное описание")
    muscle_groups = models.ManyToManyField(MuscleGroup, verbose_name="Группы мышц")
    # Дополнительные поля
    difficulty = models.CharField(max_length=50, choices=[
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ], verbose_name="Сложность")
    equipment = models.TextField(blank=True, verbose_name="Необходимое оборудование")
    execution_steps = models.TextField(verbose_name="Шаги выполнения")
    # video_url = models.URLField(blank=True, verbose_name="Ссылка на видео")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"


class Workout(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название тренировки")
    creator = models.ForeignKey(TempUser, on_delete=models.CASCADE, verbose_name="Создатель")
    is_premade = models.BooleanField(default=False, verbose_name="Готовая тренировка?")
    description = models.TextField(blank=True, verbose_name="Описание тренировки")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Для плана: day_of_week = models.IntegerField(choices=[(1, 'Понедельник'), ...], null=True, blank=True)

    def __str__(self):
        return f"{self.name} (by {self.creator})"

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"


class WorkoutExercise(models.Model):  # Промежуточная модель для упражнений в тренировке
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="workout_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name="Упражнение")
    # Порядок выполнения внутри тренировки
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    sets = models.PositiveIntegerField(default=3, verbose_name="Количество подходов")
    reps = models.CharField(max_length=50, default="10-12", verbose_name="Количество повторений (например, 10-12)")
    rest_seconds = models.PositiveIntegerField(default=60, verbose_name="Отдых (секунды)")

    class Meta:
        ordering = ['order']
        verbose_name = "Упражнение в тренировке"
        verbose_name_plural = "Упражнения в тренировках"

    def __str__(self):
        return f"{self.exercise.name} in {self.workout.name}"


class FavoriteExercise(models.Model):
    user = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name="favorite_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="favorites")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'exercise')  # Чтобы одно упражнение нельзя было добавить дважды
        verbose_name = "Избранное упражнение"
        verbose_name_plural = "Избранные упражнения"

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name}"


class Profile(models.Model):
    # OneToOne связь со встроенной моделью User
    user = models.OneToOneField(TempUser, on_delete=models.CASCADE, primary_key=True, related_name="profile")
    full_name = models.CharField(max_length=200, blank=True, verbose_name="ФИО")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Вес (кг)")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Рост (см)")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Возраст")
    total_workouts = models.PositiveIntegerField(default=0, verbose_name="Всего тренировок")
    total_exercises_done = models.PositiveIntegerField(default=0, verbose_name="Всего выполнено упражнений")
    last_workout_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата последней тренировки")

    def __str__(self):
        return f"Профиль: {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class WorkoutHistory(models.Model):
    user = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name="workout_history")
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, verbose_name="Тренировка")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время завершения")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (минуты)")
    # Дополнительно: notes = models.TextField(blank=True, verbose_name="Заметки")

    def __str__(self):
        return f"{self.user.username} - {self.workout} - {self.completed_at.date()}"

    class Meta:
        verbose_name = "История тренировок"
        verbose_name_plural = "История тренировок"
        ordering = ['-completed_at']


class PlanDay(models.Model):
    DAYS_OF_WEEK = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]
    user = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name="training_plan")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name="День недели")
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Группа мышц")
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тренировка")

    class Meta:
        unique_together = ('user', 'day_of_week')  # У пользователя может быть только один план на день
        ordering = ['day_of_week']
        verbose_name = "День плана"
        verbose_name_plural = "План тренировок"

    def __str__(self):
        return f"{self.user.username} - {self.get_day_of_week_display()}: {self.muscle_group or self.workout}"