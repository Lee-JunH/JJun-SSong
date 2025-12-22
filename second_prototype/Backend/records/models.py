from django.db import models
from django.conf import settings
from django.db.models import Sum


class DayRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()

    # 요약(월 조회용)
    total_kcal = models.FloatField(default=0)
    total_carb = models.FloatField(default=0)
    total_protein = models.FloatField(default=0)
    total_fat = models.FloatField(default=0)
    total_sugar = models.FloatField(default=0)
    total_sodium = models.FloatField(default=0)

    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    nutrition = models.BooleanField(default=False)
    condition_emoji = models.CharField(max_length=10, blank=True)  # 😊 😐 😫 등

    class Meta:
        unique_together = ("user", "date")
        indexes = [models.Index(fields=["user", "date"])]

    def recompute_summary(self):
        agg = self.meals.aggregate(
            kcal=Sum("kcal"),
            carb=Sum("carb"),
            protein=Sum("protein"),
            fat=Sum("fat"),
            sugar=Sum("sugar"),
            sodium=Sum("sodium"),
        )
        self.total_kcal = agg["kcal"] or 0
        self.total_carb = agg["carb"] or 0
        self.total_protein = agg["protein"] or 0
        self.total_fat = agg["fat"] or 0
        self.total_sugar = agg["sugar"] or 0
        self.total_sodium = agg["sodium"] or 0
        self.save(
            update_fields=[
                "total_kcal",
                "total_carb",
                "total_protein",
                "total_fat",
                "total_sugar",
                "total_sodium",
            ]
        )


MEAL_TYPES = [
    ("breakfast", "아침"),
    ("lunch", "점심"),
    ("dinner", "저녁"),
]


class MealItem(models.Model):
    day = models.ForeignKey(DayRecord, related_name="meals", on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)

    name = models.CharField(max_length=100)  # 음식명(검색 결과 복사 or 커스텀)
    grams = models.FloatField(default=0)

    # 계산된 영양(해당 grams 기준)
    kcal = models.FloatField(default=0)
    carb = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    sodium = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class ExerciseItem(models.Model):
    day = models.ForeignKey(
        DayRecord, related_name="exercises", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    minutes = models.PositiveIntegerField(default=0)
    burned_kcal = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class WeightEntry(models.Model):
    day = models.OneToOneField(
        DayRecord, related_name="weight", on_delete=models.CASCADE
    )
    weight_kg = models.FloatField()


class ConditionEntry(models.Model):
    day = models.OneToOneField(
        DayRecord, related_name="condition", on_delete=models.CASCADE
    )
    emoji = models.CharField(max_length=10)
    note = models.TextField(blank=True)
