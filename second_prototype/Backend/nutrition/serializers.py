from rest_framework import serializers
from .models import Food, CustomFood, FoodFavorite

class FoodSearchItemSerializer(serializers.Serializer):
    source = serializers.CharField()
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    per_100g_kcal = serializers.FloatField()
    per_100g_carb = serializers.FloatField()
    per_100g_protein = serializers.FloatField()
    per_100g_fat = serializers.FloatField()
    per_100g_sugar = serializers.FloatField()
    per_100g_sodium = serializers.FloatField()

class CustomFoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFood
        fields = ["id","name","per_100g_kcal","per_100g_carb","per_100g_protein","per_100g_fat","per_100g_sugar","per_100g_sodium"]

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodFavorite
        fields = ["id","name","per_100g_kcal","per_100g_carb","per_100g_protein","per_100g_fat","per_100g_sugar","per_100g_sodium","created_at"]
