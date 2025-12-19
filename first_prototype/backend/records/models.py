from django.db import models
from django.conf import settings
from foods.models import Food, CustomFood


class Meal(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = "breakfast", "아침"
        LUNCH = "lunch", "점심"
        DINNER = "dinner", "저녁"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meals"
    )
    date = models.DateField(db_index=True)
    meal_type = models.CharField(max_length=20, choices=MealType.choices)

    class Meta:
        unique_together = ("user", "date", "meal_type")
        indexes = [
            models.Index(fields=["user", "date"]),
        ]


class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="items")

    food = models.ForeignKey(Food, null=True, blank=True, on_delete=models.SET_NULL)
    custom_food = models.ForeignKey(
        CustomFood, null=True, blank=True, on_delete=models.SET_NULL
    )

    amount_g = models.FloatField()

    kcal = models.FloatField()
    carb_g = models.FloatField()
    protein_g = models.FloatField()
    fat_g = models.FloatField()
    sugar_g = models.FloatField(default=0.0)
    sodium_mg = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)


class ExerciseRecord(models.Model):
    class Intensity(models.TextChoices):
        LOW = "low", "낮음"
        MID = "mid", "보통"
        HIGH = "high", "높음"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exercises"
    )
    date = models.DateField(db_index=True)
    name = models.CharField(max_length=100)
    minutes = models.PositiveSmallIntegerField()
    intensity = models.CharField(
        max_length=10, choices=Intensity.choices, default=Intensity.MID
    )
    estimated_kcal = models.FloatField(default=0.0)


class WeightRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weights"
    )
    date = models.DateField(db_index=True)
    weight_kg = models.FloatField()

    class Meta:
        unique_together = ("user", "date")


class ConditionRecord(models.Model):
    class Mood(models.TextChoices):
        GOOD = "good", "좋음"
        OK = "ok", "보통"
        BAD = "bad", "나쁨"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conditions"
    )
    date = models.DateField(db_index=True)
    mood = models.CharField(max_length=10, choices=Mood.choices)

    class Meta:
        unique_together = ("user", "date")


class SupplementIntake(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supplements"
    )
    date = models.DateField(db_index=True)
    taken = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "date")
