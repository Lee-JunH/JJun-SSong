from django.db import models
from django.conf import settings

class Food(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    per_100g_kcal = models.FloatField(default=0)
    per_100g_carb = models.FloatField(default=0)
    per_100g_protein = models.FloatField(default=0)
    per_100g_fat = models.FloatField(default=0)
    per_100g_sugar = models.FloatField(default=0)
    per_100g_sodium = models.FloatField(default=0)

class CustomFood(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    per_100g_kcal = models.FloatField(default=0)
    per_100g_carb = models.FloatField(default=0)
    per_100g_protein = models.FloatField(default=0)
    per_100g_fat = models.FloatField(default=0)
    per_100g_sugar = models.FloatField(default=0)
    per_100g_sodium = models.FloatField(default=0)

class FoodFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    per_100g_kcal = models.FloatField(default=0)
    per_100g_carb = models.FloatField(default=0)
    per_100g_protein = models.FloatField(default=0)
    per_100g_fat = models.FloatField(default=0)
    per_100g_sugar = models.FloatField(default=0)
    per_100g_sodium = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user", "name"])]
