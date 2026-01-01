from django.contrib import admin
from main.models import MuscleGroup, Exercise, Workout, WorkoutHistory, PlanDay, WorkoutExercise, FavoriteExercise, Profile, TempUser
# Register your models here.

admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(WorkoutHistory)
admin.site.register(PlanDay)
admin.site.register(WorkoutExercise)
admin.site.register(FavoriteExercise)
admin.site.register(Profile)
admin.site.register(TempUser)