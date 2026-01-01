from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercise, MuscleGroup, FavoriteExercise, Workout, WorkoutExercise
from .models import TempUser  # потом заменить на нормальную авторизацию Денисовидную

# Create your views here.

def get_temp_user():
    return TempUser.objects.first()

# МЕНЯЮ ВСЕ request.user и user.is_authenticated НА ТЕМП ЮСЕР, ПОТОМ ВЕРНУТЬ ОБРАТНО


def exercise_list(request):  # список упражнений и филтрация по группам мышц
    muscle_groups = MuscleGroup.objects.all()
    exercises = Exercise.objects.all()

    muscle_group_id = request.GET.get("muscle_group")  # из юрл берем параметр
    if muscle_group_id:
        exercises = exercises.filter(
            muscle_groups__id=muscle_group_id
        )  # если филтрация выбрана то оставляем упражнения у которых есть группа мышц с таким айди

    return render(
        request,
        "exercises/exercise_list.html",
        {"exercises": exercises, "muscle_groups": muscle_groups},
    )


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    #is_favorite = False                                ПОТОМ ВЕРНУТЬ
    #if (
    #    request.user.is_authenticated
    #):  # зареган ли пользователь, если да, проверяет есть ли избранное
    #    is_favorite = FavoriteExercise.objects.filter(
    #        user=request.user, exercise=exercise
    #    ).exists()  # exists возвращает true false

    user = get_temp_user()    #                         ПОТОМ УДАЛИТЬ
    is_favorite = FavoriteExercise.objects.filter(
        user=user, exercise=exercise
    ).exists()

    return render(
        request,
        "exercises/exercise_detail.html",
        {"exercise": exercise, "is_favorite": is_favorite},
    )


def toggle_favorite(request, exercise_id):
    #if not request.user.is_authenticated:  # если гость = на авторизацию               ВЕРНУТЬ
    #    return redirect("login")

    exercise = get_object_or_404(Exercise, id=exercise_id)

    #favorite, created = (                                                  ВЕРНУТЬ
    #    FavoriteExercise.objects.get_or_create(  # get_or_create - если запись есть -> вернуть ее, если нет - создать
    #        user=request.user, exercise=exercise
    #    )
    #)

    user = get_temp_user()

    favorite, created = FavoriteExercise.objects.get_or_create(
        user=user,
        exercise=exercise
    )

    if not created:
        favorite.delete()

    return redirect("exercise_detail", exercise_id=exercise.id)


def workout_list(request):
    #if not request.user.is_authenticated:                                            ВЕРНУТЬ
    #    return redirect("login")

    #workouts = Workout.objects.filter(creator=request.user)

    user = get_temp_user()
    workouts = Workout.objects.filter(creator=user)

    return render(request, "workouts/workout_list.html", {"workouts": workouts})


def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    exercises = WorkoutExercise.objects.filter(workout=workout)

    return render(
        request,
        "workouts/workout_detail.html",
        {"workout": workout, "exercises": exercises},
    )


def workout_create(request):
    #if not request.user.is_authenticated:                              ВЕРНУТЬ
    #    return redirect("login")
    user = get_temp_user()

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        #workout = Workout.objects.create( # создается таблица в бд для тренировки      ВЕРНУТЬ
        #    name=name,
        #    description=description,
        #    creator=request.user,
        #    is_premade=False # пользовательская тренировка
        #)
        workout = Workout.objects.create(
            name=name,
            description=description,
            creator = user,
            is_premade=False
        )

        return redirect("workout_detail", workout_id=workout.id)

    return render(request, "workouts/workout_create.html")

def add_exercise_to_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    exercises = Exercise.objects.all()

    if request.method == "POST":
        exercise_id = request.POST.get("exercise")
        sets = request.POST.get("sets", 3)
        reps = request.POST.get("reps", "10-12")

        WorkoutExercise.objects.create(
            workout=workout,
            exercise_id=exercise_id,
            sets=sets,
            reps=reps
        )

        return redirect('workout_detail', workout_id=workout_id)

    return render(request, "workouts/add_exercise.html", {
        "workout": workout,
        "exercises": exercises
    })

