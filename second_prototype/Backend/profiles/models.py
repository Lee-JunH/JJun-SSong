from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    gender = models.CharField(max_length=10, blank=True)  # 'male'/'female'
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # cm
    weight = models.FloatField(null=True, blank=True)  # kg
    start_weight = models.FloatField(null=True, blank=True)  # kg
    goal_weight = models.FloatField(null=True, blank=True)  # kg
    activity_level = models.PositiveSmallIntegerField(null=True, blank=True)  # 1~5

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile<{self.user_id}>"
