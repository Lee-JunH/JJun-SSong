from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "gender",
            "age",
            "height",
            "weight",
            "start_weight",
            "goal_weight",
            "activity_level",
            "updated_at",
        ]
