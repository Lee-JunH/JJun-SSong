from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "height_cm",
            "current_weight_kg",
            "age",
            "sex",
            "activity_level",
            "start_weight_kg",
            "goal_weight_kg",
        ]

    def validate_height_cm(self, v):
        if v is None:
            return v
        if not (50 <= v <= 250):
            raise serializers.ValidationError("키는 50~250cm 범위여야 합니다.")
        return v

    def validate_age(self, v):
        if v is None:
            return v
        if not (1 <= v <= 120):
            raise serializers.ValidationError("나이는 1~120 범위여야 합니다.")
        return v

    def validate(self, attrs):
        # 몸무게 범위(필요 시 조정)
        for k in ["current_weight_kg", "start_weight_kg", "goal_weight_kg"]:
            if k in attrs and attrs[k] is not None:
                if not (10 <= float(attrs[k]) <= 300):
                    raise serializers.ValidationError(
                        {k: "몸무게는 10~300kg 범위여야 합니다."}
                    )
        return attrs
