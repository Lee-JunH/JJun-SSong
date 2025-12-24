from django.conf import settings
from django.db import models


class NutritionBase(models.Model):
    """공통 영양 필드(데이터셋/커스텀/즐겨찾기에서 재사용)."""

    name = models.CharField(max_length=255, db_index=True)

    # loaddata fixture에서 문자열("78.0")로 들어와도 DecimalField는 안전하게 파싱됩니다.
    energy_kcal = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    carbs_g = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    protein_g = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    fat_g = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    sugars_g = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    sodium_mg = models.DecimalField(max_digits=9, decimal_places=1, default=0)

    class Meta:
        abstract = True


class Food(NutritionBase):
    """고정(공용) 데이터셋용 테이블"""

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="uq_food_name"),
        ]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class CustomFood(NutritionBase):
    """사용자가 직접 추가한 음식"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="custom_foods"
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="uq_customfood_user_name"
            ),
        ]
        indexes = [
            models.Index(fields=["user", "name"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.user_id})"


class FoodFavorite(NutritionBase):
    """즐겨찾기(스냅샷 저장 방식: 저장 시점의 값을 그대로 보관)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="food_favorites",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["user", "name"]),
        ]
