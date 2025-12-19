from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    class Goal(models.TextChoices):
        CUT = "cut", "감량"
        MAINTAIN = "maintain", "유지"
        BULK = "bulk", "증량"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    height_cm = models.PositiveSmallIntegerField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)  # "M"/"F"/etc
    goal = models.CharField(max_length=20, choices=Goal.choices, default=Goal.MAINTAIN)

    def __str__(self):
        return f"{self.user.email} profile"
