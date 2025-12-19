from django.db import models
from django.conf import settings


class Food(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    serving_g = models.FloatField(default=100.0)

    kcal = models.FloatField()
    carb_g = models.FloatField()
    protein_g = models.FloatField()
    fat_g = models.FloatField()
    sugar_g = models.FloatField(default=0.0)
    sodium_mg = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class CustomFood(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="custom_foods"
    )
    name = models.CharField(max_length=200, db_index=True)
    serving_g = models.FloatField(default=100.0)

    kcal = models.FloatField()
    carb_g = models.FloatField()
    protein_g = models.FloatField()
    fat_g = models.FloatField()
    sugar_g = models.FloatField(default=0.0)
    sodium_mg = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (custom)"
