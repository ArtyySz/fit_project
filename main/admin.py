from django.contrib import admin
from .models import (
    MuscleGroup,
    Exercise,
    Workout,
    WorkoutHistory,
    PlanDay,
    WorkoutExercise,
    FavoriteExercise,
    Profile
)

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "difficulty")
    list_filter = ("difficulty", "muscle_groups")
    search_fields = ("name", "description", "equipment", "execution_steps")
    filter_horizontal = ("muscle_groups",)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "creator", "is_premade", "created_at")
    list_filter = ("is_premade", "created_at")
    search_fields = ("name", "description", "creator__username")
    inlines = [WorkoutExerciseInline]


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "workout", "exercise", "sets", "reps", "rest_seconds", "order")
    list_filter = ("workout",)
    search_fields = ("workout__name", "exercise__name")


@admin.register(WorkoutHistory)
class WorkoutHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "workout", "duration_minutes", "completed_at")
    list_filter = ("completed_at",)
    search_fields = ("user__username", "workout__name")


@admin.register(PlanDay)
class PlanDayAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "day_of_week", "workout", "muscle_group")
    list_filter = ("day_of_week",)
    search_fields = ("user__username", "workout__name")


@admin.register(FavoriteExercise)
class FavoriteExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "exercise", "added_at")
    list_filter = ("added_at",)
    search_fields = ("user__username", "exercise__name")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "full_name",
        "age",
        "weight",
        "height",
        "total_workouts",
        "total_exercises_done",
        "last_workout_date",
    )
    search_fields = ("user__username", "full_name")