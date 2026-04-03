from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import (
    ProfileForm,
    WorkoutForm,
    WorkoutExerciseForm,
    PlanDayForm,
    CompleteWorkoutForm,
)

from .models import (
    Exercise,
    MuscleGroup,
    FavoriteExercise,
    Workout,
    WorkoutExercise,
    WorkoutHistory,
    PlanDay,
)
from .forms import ProfileForm


def index(request):
    popular_exercises = Exercise.objects.annotate(
        fav_count=Count("favorites")
    ).order_by("-fav_count")[:5]

    if request.user.is_authenticated:
        last_workouts = WorkoutHistory.objects.filter(
            user=request.user
        ).select_related("workout")[:5]

        workouts_count = WorkoutHistory.objects.filter(
            user=request.user
        ).count()
    else:
        last_workouts = []
        workouts_count = 0

    return render(request, "main/index.html", {
        "popular_exercises": popular_exercises,
        "last_workouts": last_workouts,
        "workouts_count": workouts_count,
    })


def exercise_list(request):
    muscle_groups = MuscleGroup.objects.all()
    exercises = Exercise.objects.all()

    # Получаем параметры из URL
    muscle_group_id = request.GET.get("muscle_group")
    difficulty = request.GET.get("difficulty")
    search = request.GET.get("search")
    sort = request.GET.get("sort")

    # Фильтр по группе мышц
    if muscle_group_id:
        exercises = exercises.filter(muscle_groups__id=muscle_group_id)

    # Фильтр по сложности
    if difficulty:
        exercises = exercises.filter(difficulty=difficulty)

    # Поиск по названию
    if search:
        exercises = exercises.filter(name__icontains=search)

    # Сортировка
    if sort == "name_asc":
        exercises = exercises.order_by("name")
    elif sort == "name_desc":
        exercises = exercises.order_by("-name")

    return render(request, "exercises/exercise_list.html", {
        "exercises": exercises.distinct(),
        "muscle_groups": muscle_groups,
        "selected_muscle_group": muscle_group_id,
        "selected_difficulty": difficulty,
        "search_query": search,
        "selected_sort": sort,
    })


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteExercise.objects.filter(
            user=request.user,
            exercise=exercise
        ).exists()

    return render(request, "exercises/exercise_detail.html", {
        "exercise": exercise,
        "is_favorite": is_favorite,
    })


@login_required
def toggle_favorite(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    favorite, created = FavoriteExercise.objects.get_or_create(
        user=request.user,
        exercise=exercise
    )

    if not created:
        favorite.delete()

    return redirect("exercise_detail", exercise_id=exercise.id)


# -------------------- ТРЕНИРОВКИ --------------------
@login_required
def workout_list(request):
    workouts = Workout.objects.filter(creator=request.user)
    return render(request, "workouts/workout_list.html", {"workouts": workouts})


@login_required
def workout_create(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.creator = request.user
            workout.is_premade = False
            workout.save()
            return redirect("workout_detail", workout_id=workout.id)
    else:
        form = WorkoutForm()

    return render(request, "workouts/workout_create.html", {
        "form": form
    })

@login_required
def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)

    # Разрешаем открыть:
    # 1) свои тренировки
    # 2) готовые тренировки
    if not workout.is_premade and workout.creator != request.user:
        return redirect("workout_list")

    exercises = WorkoutExercise.objects.filter(workout=workout)

    return render(request, "workouts/workout_detail.html", {
        "workout": workout,
        "exercises": exercises,
    })

@login_required
def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, creator=request.user)

    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workout_detail", workout_id=workout.id)
    else:
        form = WorkoutForm(instance=workout)

    return render(request, "workouts/edit_workout.html", {
        "form": form,
        "workout": workout
    })

@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, creator=request.user)

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return redirect("workout_detail", workout_id=workout.id)


@login_required
def add_exercise_to_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, creator=request.user)

    if request.method == "POST":
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            workout_exercise = form.save(commit=False)
            workout_exercise.workout = workout
            workout_exercise.save()
            return redirect("workout_detail", workout_id=workout.id)
    else:
        form = WorkoutExerciseForm()

    return render(request, "workouts/add_exercise.html", {
        "workout": workout,
        "form": form,
    })


@login_required
def delete_workout_exercise(request, workout_exercise_id):
    workout_exercise = get_object_or_404(
        WorkoutExercise,
        id=workout_exercise_id,
        workout__creator=request.user
    )

    workout_id = workout_exercise.workout.id

    if request.method == "POST":
        workout_exercise.delete()

    return redirect("workout_detail", workout_id=workout_id)


@login_required
def complete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, creator=request.user)
    exercises_count = WorkoutExercise.objects.filter(workout=workout).count()

    if request.method == "POST":
        form = CompleteWorkoutForm(request.POST)
        if form.is_valid():
            duration = form.cleaned_data["duration_minutes"]

            WorkoutHistory.objects.create(
                user=request.user,
                workout=workout,
                duration_minutes=duration
            )

            profile = request.user.profile
            profile.total_workouts += 1
            profile.total_exercises_done += exercises_count
            latest_history = WorkoutHistory.objects.filter(user=request.user).first()
            if latest_history:
                profile.last_workout_date = latest_history.completed_at
            profile.save()

            return redirect("profile")
    else:
        form = CompleteWorkoutForm()

    return render(request, "workouts/complete_workout.html", {
        "workout": workout,
        "exercises_count": exercises_count,
        "form": form,
    })


@login_required
def plan_list(request):
    plan_days = PlanDay.objects.filter(user=request.user).select_related("workout")

    existing_days = {item.day_of_week for item in plan_days}

    for day_num, _ in PlanDay.DAYS_OF_WEEK:
        if day_num not in existing_days:
            PlanDay.objects.create(user=request.user, day_of_week=day_num)

    plan_days = PlanDay.objects.filter(user=request.user).select_related("workout")

    return render(request, "plan/plan_list.html", {
        "plan_days": plan_days
    })


@login_required
def edit_plan_day(request, plan_day_id):
    plan_day = get_object_or_404(PlanDay, id=plan_day_id, user=request.user)
    workouts = Workout.objects.filter(creator=request.user)

    if request.method == "POST":
        form = PlanDayForm(request.POST, instance=plan_day)
        form.fields["workout"].queryset = workouts

        if form.is_valid():
            form.save()
            return redirect("plan_list")
    else:
        form = PlanDayForm(instance=plan_day)
        form.fields["workout"].queryset = workouts

    return render(request, "plan/edit_plan_day.html", {
        "plan_day": plan_day,
        "form": form,
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "auth/register.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "profile/profile.html")


@login_required
def edit_profile(request):
    profile = getattr(request.user, "profile", None)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile/edit.html", {"form": form})

@login_required
def favorite_exercises(request):
    favorites = FavoriteExercise.objects.filter(
        user=request.user
    ).select_related("exercise")

    return render(request, "exercises/favorites.html", {
        "favorites": favorites
    })

@login_required
def premade_workouts(request):
    workouts = Workout.objects.filter(is_premade=True)
    return render(request, "workouts/premade_workouts.html", {
        "workouts": workouts
    })


@login_required
def copy_premade_workout(request, workout_id):
    premade = get_object_or_404(Workout, id=workout_id, is_premade=True)

    # создаём копию тренировки
    new_workout = Workout.objects.create(
        name=premade.name,
        description=premade.description,
        creator=request.user,
        is_premade=False
    )

    # копируем упражнения
    premade_exercises = WorkoutExercise.objects.filter(workout=premade)

    for item in premade_exercises:
        WorkoutExercise.objects.create(
            workout=new_workout,
            exercise=item.exercise,
            order=item.order,
            sets=item.sets,
            reps=item.reps,
            rest_seconds=item.rest_seconds
        )

    return redirect("workout_detail", workout_id=new_workout.id)

@login_required
def workout_history_list(request):
    history = WorkoutHistory.objects.filter(
        user=request.user
    ).select_related("workout").order_by("-completed_at")

    return render(request, "history/history_list.html", {
        "history": history
    })

@login_required
def workout_history_detail(request, history_id):
    history_item = get_object_or_404(
        WorkoutHistory,
        id=history_id,
        user=request.user
    )

    workout_exercises = WorkoutExercise.objects.filter(
        workout=history_item.workout
    ).select_related("exercise")

    return render(request, "history/history_detail.html", {
        "history_item": history_item,
        "workout_exercises": workout_exercises,
    })

@login_required
def premade_workouts(request):
    workouts = Workout.objects.filter(is_premade=True)
    return render(request, "workouts/premade_workouts.html", {
        "workouts": workouts
    })


@login_required
def copy_premade_workout(request, workout_id):
    premade_workout = get_object_or_404(Workout, id=workout_id, is_premade=True)

    # Копируем саму тренировку
    new_workout = Workout.objects.create(
        name=premade_workout.name,
        description=premade_workout.description,
        creator=request.user,
        is_premade=False
    )

    # Копируем упражнения
    premade_exercises = WorkoutExercise.objects.filter(workout=premade_workout)

    for item in premade_exercises:
        WorkoutExercise.objects.create(
            workout=new_workout,
            exercise=item.exercise,
            order=item.order,
            sets=item.sets,
            reps=item.reps,
            rest_seconds=item.rest_seconds,
        )

    return redirect("workout_detail", workout_id=new_workout.id)