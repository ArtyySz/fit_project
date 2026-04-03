from django import forms
from .models import Profile, Workout, WorkoutExercise, PlanDay


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "age", "weight", "height"]

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and (age < 10 or age > 120):
            raise forms.ValidationError("Возраст должен быть от 10 до 120.")
        return age

    def clean_weight(self):
        weight = self.cleaned_data.get("weight")
        if weight is not None and (weight < 20 or weight > 400):
            raise forms.ValidationError("Вес должен быть от 20 до 400 кг.")
        return weight

    def clean_height(self):
        height = self.cleaned_data.get("height")
        if height is not None and (height < 50 or height > 300):
            raise forms.ValidationError("Рост должен быть от 50 до 300 см.")
        return height


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["name", "description"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name or len(name.strip()) < 2:
            raise forms.ValidationError("Название тренировки должно быть минимум 2 символа.")
        return name.strip()


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ["exercise", "sets", "reps", "rest_seconds"]

    def clean_sets(self):
        sets = self.cleaned_data.get("sets")
        if sets < 1 or sets > 20:
            raise forms.ValidationError("Подходов должно быть от 1 до 20.")
        return sets

    def clean_reps(self):
        reps = self.cleaned_data.get("reps")
        if not reps or len(reps.strip()) < 1:
            raise forms.ValidationError("Укажи количество повторений.")
        return reps.strip()

    def clean_rest_seconds(self):
        rest = self.cleaned_data.get("rest_seconds")
        if rest < 0 or rest > 1800:
            raise forms.ValidationError("Отдых должен быть от 0 до 1800 секунд.")
        return rest


class PlanDayForm(forms.ModelForm):
    class Meta:
        model = PlanDay
        fields = ["workout"]


class CompleteWorkoutForm(forms.Form):
    duration_minutes = forms.IntegerField(
        min_value=1,
        max_value=600,
        label="Длительность (минуты)"
    )