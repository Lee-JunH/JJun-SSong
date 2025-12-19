from rest_framework import serializers
from datetime import date as dt_date

from .models import (
    Meal,
    MealItem,
    ExerciseRecord,
    WeightRecord,
    ConditionRecord,
    SupplementIntake,
)
from foods.models import Food, CustomFood
from .services import scale_nutrients, estimate_exercise_kcal


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ("id", "date", "meal_type")


class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = (
            "id",
            "meal",
            "food",
            "custom_food",
            "amount_g",
            "kcal",
            "carb_g",
            "protein_g",
            "fat_g",
            "sugar_g",
            "sodium_mg",
            "created_at",
        )
        read_only_fields = (
            "kcal",
            "carb_g",
            "protein_g",
            "fat_g",
            "sugar_g",
            "sodium_mg",
            "created_at",
        )

    def validate(self, attrs):
        food = attrs.get("food")
        custom_food = attrs.get("custom_food")
        if (food and custom_food) or (not food and not custom_food):
            raise serializers.ValidationError(
                "food 또는 custom_food 중 하나만 지정해야 합니다."
            )
        if attrs.get("amount_g", 0) <= 0:
            raise serializers.ValidationError("amount_g는 0보다 커야 합니다.")
        return attrs

    def create(self, validated_data):
        food = validated_data.get("food")
        custom_food = validated_data.get("custom_food")
        amount_g = validated_data["amount_g"]

        if food:
            base = {
                "kcal": food.kcal,
                "carb_g": food.carb_g,
                "protein_g": food.protein_g,
                "fat_g": food.fat_g,
                "sugar_g": food.sugar_g,
                "sodium_mg": food.sodium_mg,
            }
            snap = scale_nutrients(base, food.serving_g, amount_g)
        else:
            base = {
                "kcal": custom_food.kcal,
                "carb_g": custom_food.carb_g,
                "protein_g": custom_food.protein_g,
                "fat_g": custom_food.fat_g,
                "sugar_g": custom_food.sugar_g,
                "sodium_mg": custom_food.sodium_mg,
            }
            snap = scale_nutrients(base, custom_food.serving_g, amount_g)

        return MealItem.objects.create(**validated_data, **snap)


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecord
        fields = ("id", "date", "name", "minutes", "intensity", "estimated_kcal")
        read_only_fields = ("estimated_kcal",)

    def create(self, validated_data):
        user = self.context["request"].user
        # 프로필에서 체중을 가져오고 싶다면: "해당 날짜 WeightRecord" 또는 "최근 WeightRecord"를 활용 가능
        # 프로토타입은 60kg 기본
        weight_kg = 60.0
        minutes = validated_data["minutes"]
        intensity = validated_data.get("intensity", "mid")
        estimated = estimate_exercise_kcal(minutes, intensity, weight_kg)

        return ExerciseRecord.objects.create(
            user=user, estimated_kcal=estimated, **validated_data
        )


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightRecord
        fields = ("id", "date", "weight_kg")


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionRecord
        fields = ("id", "date", "mood")


class SupplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplementIntake
        fields = ("id", "date", "taken")
