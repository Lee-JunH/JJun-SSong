from rest_framework import serializers
from .models import DayRecord, MealItem, ExerciseItem, WeightEntry, ConditionEntry


class MealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealItem
        fields = [
            "id",
            "meal_type",
            "name",
            "grams",
            "kcal",
            "carb",
            "protein",
            "fat",
            "sugar",
            "sodium",
            "created_at",
        ]


class ExerciseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseItem
        fields = ["id", "name", "minutes", "burned_kcal", "created_at"]


class WeightEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ["weight_kg"]


class ConditionEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionEntry
        fields = ["emoji", "note"]


class DaySummarySerializer(serializers.ModelSerializer):
    has_meal = serializers.SerializerMethodField()
    has_exercise = serializers.SerializerMethodField()
    has_weight = serializers.SerializerMethodField()
    warning_flags = serializers.SerializerMethodField()

    class Meta:
        model = DayRecord
        fields = [
            "date",
            "has_meal",
            "has_exercise",
            "has_weight",
            "condition_emoji",
            "breakfast",
            "lunch",
            "dinner",
            "nutrition",
            "total_kcal",
            "total_carb",
            "total_protein",
            "total_fat",
            "total_sugar",
            "total_sodium",
            "warning_flags",
        ]

    def get_has_meal(self, obj):
        return obj.meals.exists()

    def get_has_exercise(self, obj):
        return obj.exercises.exists()

    def get_has_weight(self, obj):
        return hasattr(obj, "weight")

    def get_warning_flags(self, obj):
        flags = []
        # 기준치는 추후 사용자 목표/권장량 테이블로 확장 가능
        if obj.total_sugar >= 50:
            flags.append("HIGH_SUGAR")
        if obj.total_sodium >= 2000:
            flags.append("HIGH_SODIUM")
        return flags


class DayDetailSerializer(serializers.ModelSerializer):
    meals = MealItemSerializer(many=True, read_only=True)
    exercises = ExerciseItemSerializer(many=True, read_only=True)
    weight = WeightEntrySerializer(read_only=True)
    condition = ConditionEntrySerializer(read_only=True)

    class Meta:
        model = DayRecord
        fields = [
            "date",
            "total_kcal",
            "total_carb",
            "total_protein",
            "total_fat",
            "total_sugar",
            "total_sodium",
            "condition_emoji",
            "breakfast",
            "lunch",
            "dinner",
            "nutrition",
            "meals",
            "exercises",
            "weight",
            "condition",
        ]
