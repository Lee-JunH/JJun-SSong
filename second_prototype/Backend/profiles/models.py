from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    SEX_CHOICES = [
        ("M", "남"),
        ("F", "여"),
        ("O", "기타/선택안함"),
    ]

    ACTIVITY_CHOICES = [
        ("sedentary", "거의 안 함"),
        ("light", "가벼움(주 1~3회)"),
        ("moderate", "보통(주 3~5회)"),
        ("active", "활발(주 6~7회)"),
        ("very_active", "매우 활발(고강도/2회 이상)"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    height_cm = models.PositiveSmallIntegerField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, default="O")
    activity_level = models.CharField(
        max_length=20, choices=ACTIVITY_CHOICES, default="sedentary"
    )

    current_weight_kg = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    start_weight_kg = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    goal_weight_kg = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id} profile"
