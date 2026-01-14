from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("exercises/", views.exercise_list, name="exercise_list"),
    path("exercises/<int:exercise_id>/", views.exercise_detail, name="exercise_detail"),
    path("exercises/<int:exercise_id>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("workouts/", views.workout_list, name="workout_list"),
    path("workouts/create/", views.workout_create, name="workout_create"),
    path("workouts/<int:workout_id>/", views.workout_detail, name="workout_detail"),
    path("workouts/<int:workout_id>/add-exercise/", views.add_exercise_to_workout, name="add_exercise_to_workout"),
]
