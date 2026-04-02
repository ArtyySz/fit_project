from django.urls import path
from . import views
from .views import index
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", index, name="index"),

    path("exercises/", views.exercise_list, name="exercise_list"),
    path("exercises/<int:exercise_id>/", views.exercise_detail, name="exercise_detail"),
    path("exercises/<int:exercise_id>/favorite/", views.toggle_favorite, name="toggle_favorite"),

    path("workouts/", views.workout_list, name="workout_list"),
    path("workouts/create/", views.workout_create, name="workout_create"),
    path("workouts/<int:workout_id>/", views.workout_detail, name="workout_detail"),
    path("workouts/<int:workout_id>/edit/", views.edit_workout, name="edit_workout"),
    path("workouts/<int:workout_id>/delete/", views.delete_workout, name="delete_workout"),
    path("workouts/<int:workout_id>/add-exercise/", views.add_exercise_to_workout, name="add_exercise_to_workout"),
    path("workout-exercise/<int:workout_exercise_id>/delete/", views.delete_workout_exercise, name="delete_workout_exercise"),
    path("workouts/<int:workout_id>/complete/", views.complete_workout, name="complete_workout"),

    path("plan/", views.plan_list, name="plan_list"),
    path("plan/<int:plan_day_id>/edit/", views.edit_plan_day, name="edit_plan_day"),

    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("favorites/", views.favorite_exercises, name="favorite_exercises"),

    path("premade-workouts/", views.premade_workouts, name="premade_workouts"),
    path("premade-workouts/<int:workout_id>/copy/", views.copy_premade_workout, name="copy_premade_workout"),
    path("history/", views.workout_history_list, name="workout_history_list"),
    path("history/<int:history_id>/", views.workout_history_detail, name="workout_history_detail"),
    path("premade-workouts/", views.premade_workouts, name="premade_workouts"),
    path("premade-workouts/<int:workout_id>/copy/", views.copy_premade_workout, name="copy_premade_workout"),
]