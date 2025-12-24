from rest_framework import serializers
from .models import Food, CustomFood, FoodFavorite


class FoodSearchItemSerializer(serializers.Serializer):
    """검색 응답(공용 Food + CustomFood 통합)용"""

    source = serializers.ChoiceField(choices=["public", "custom"])
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()

    energy_kcal = serializers.DecimalField(max_digits=8, decimal_places=1)
    carbs_g = serializers.DecimalField(max_digits=8, decimal_places=1)
    protein_g = serializers.DecimalField(max_digits=8, decimal_places=1)
    fat_g = serializers.DecimalField(max_digits=8, decimal_places=1)
    sugars_g = serializers.DecimalField(max_digits=8, decimal_places=1)
    sodium_mg = serializers.DecimalField(max_digits=9, decimal_places=1)


class CustomFoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFood
        fields = [
            "id",
            "name",
            "energy_kcal",
            "carbs_g",
            "protein_g",
            "fat_g",
            "sugars_g",
            "sodium_mg",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodFavorite
        fields = [
            "id",
            "name",
            "energy_kcal",
            "carbs_g",
            "protein_g",
            "fat_g",
            "sugars_g",
            "sodium_mg",
            "created_at",
        ]
