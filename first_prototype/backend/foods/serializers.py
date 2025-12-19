from rest_framework import serializers
from .models import Food, CustomFood


class FoodSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = (
            "id",
            "name",
            "serving_g",
            "kcal",
            "carb_g",
            "protein_g",
            "fat_g",
            "sugar_g",
            "sodium_mg",
            "source",
        )

    def get_source(self, obj):
        return "dataset"


class CustomFoodSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = CustomFood
        fields = (
            "id",
            "name",
            "serving_g",
            "kcal",
            "carb_g",
            "protein_g",
            "fat_g",
            "sugar_g",
            "sodium_mg",
            "source",
        )

    def get_source(self, obj):
        return "custom"

    def create(self, validated_data):
        request = self.context["request"]
        return CustomFood.objects.create(owner=request.user, **validated_data)
