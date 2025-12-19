from datetime import datetime, date
from calendar import monthrange

from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound

from .models import (
    Meal,
    MealItem,
    ExerciseRecord,
    WeightRecord,
    ConditionRecord,
    SupplementIntake,
)
from .serializers import (
    MealSerializer,
    MealItemSerializer,
    ExerciseSerializer,
    WeightSerializer,
    ConditionSerializer,
    SupplementSerializer,
)

SUGAR_WARN_G = 50.0
SODIUM_WARN_MG = 2000.0


class RecordsHubViewSet(viewsets.ViewSet):
    """
    프로토타입용: records 도메인의 핵심 엔드포인트를 하나의 ViewSet으로 통합.
    """

    # ---------- helpers ----------
    def _parse_date(self, date_str: str) -> date:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise NotFound("날짜 형식은 YYYY-MM-DD 입니다.")

    def _ensure_owned_meal(self, meal: Meal):
        if meal.user_id != self.request.user.id:
            raise PermissionDenied("본인 데이터만 접근할 수 있습니다.")

    # ---------- calendar ----------
    @action(detail=False, methods=["get"], url_path="calendar")
    def calendar(self, request):
        month = request.query_params.get("month")  # "YYYY-MM"
        if not month or "-" not in month:
            return Response({"detail": "month=YYYY-MM 형식이 필요합니다."}, status=400)

        y, m = map(int, month.split("-"))
        start = date(y, m, 1)
        end = date(y, m, monthrange(y, m)[1])

        user = request.user
        days = {}

        def ensure(d):
            if d not in days:
                days[d] = {
                    "date": d.isoformat(),
                    "has_meal": False,
                    "has_exercise": False,
                    "has_weight": False,
                    "mood": None,
                    "supplement_taken": False,
                }

        for obj in Meal.objects.filter(user=user, date__range=(start, end)).only(
            "date"
        ):
            ensure(obj.date)
            days[obj.date]["has_meal"] = True

        for obj in ExerciseRecord.objects.filter(
            user=user, date__range=(start, end)
        ).only("date"):
            ensure(obj.date)
            days[obj.date]["has_exercise"] = True

        for obj in WeightRecord.objects.filter(
            user=user, date__range=(start, end)
        ).only("date"):
            ensure(obj.date)
            days[obj.date]["has_weight"] = True

        for obj in ConditionRecord.objects.filter(
            user=user, date__range=(start, end)
        ).only("date", "mood"):
            ensure(obj.date)
            days[obj.date]["mood"] = obj.mood

        for obj in SupplementIntake.objects.filter(
            user=user, date__range=(start, end), taken=True
        ).only("date"):
            ensure(obj.date)
            days[obj.date]["supplement_taken"] = True

        result = [days[d] for d in sorted(days.keys())]
        return Response({"month": month, "days": result})

    # ---------- day detail ----------
    @action(
        detail=False, methods=["get"], url_path=r"days/(?P<date_str>\d{4}-\d{2}-\d{2})"
    )
    def day_detail(self, request, date_str=None):
        d = self._parse_date(date_str)
        user = request.user

        meals = Meal.objects.filter(user=user, date=d).order_by("meal_type")
        meal_ids = list(meals.values_list("id", flat=True))

        items = (
            MealItem.objects.filter(meal_id__in=meal_ids)
            .select_related("meal", "food", "custom_food")
            .order_by("created_at")
        )

        meal_map = {m.id: {"meal": MealSerializer(m).data, "items": []} for m in meals}
        for it in items:
            meal_map[it.meal_id]["items"].append(MealItemSerializer(it).data)

        agg = items.aggregate(
            kcal=Sum("kcal"),
            carb_g=Sum("carb_g"),
            protein_g=Sum("protein_g"),
            fat_g=Sum("fat_g"),
            sugar_g=Sum("sugar_g"),
            sodium_mg=Sum("sodium_mg"),
        )
        totals = {k: float(agg[k] or 0) for k in agg}

        warnings = {
            "sugar_excess": totals["sugar_g"] >= SUGAR_WARN_G,
            "sodium_excess": totals["sodium_mg"] >= SODIUM_WARN_MG,
        }

        exercises = ExerciseRecord.objects.filter(user=user, date=d).order_by("-id")
        weight = WeightRecord.objects.filter(user=user, date=d).first()
        condition = ConditionRecord.objects.filter(user=user, date=d).first()
        supplement = SupplementIntake.objects.filter(user=user, date=d).first()

        return Response(
            {
                "date": d.isoformat(),
                "nutrition_totals": totals,
                "warnings": warnings,
                "meals": list(meal_map.values()),
                "exercises": ExerciseSerializer(
                    exercises, many=True, context={"request": request}
                ).data,
                "weight": WeightSerializer(weight).data if weight else None,
                "condition": ConditionSerializer(condition).data if condition else None,
                "supplement": SupplementSerializer(supplement).data
                if supplement
                else {"date": d.isoformat(), "taken": False},
            }
        )

    # ---------- meal upsert ----------
    @action(detail=False, methods=["post"], url_path="meals")
    def meal_upsert(self, request):
        """
        body: { "date": "YYYY-MM-DD", "meal_type": "breakfast|lunch|dinner" }
        """
        date_str = request.data.get("date")
        meal_type = request.data.get("meal_type")
        if not date_str or not meal_type:
            return Response({"detail": "date, meal_type이 필요합니다."}, status=400)

        d = self._parse_date(date_str)
        meal, created = Meal.objects.get_or_create(
            user=request.user, date=d, meal_type=meal_type
        )
        return Response(
            {"created": created, "meal": MealSerializer(meal).data}, status=200
        )

    # ---------- meal-items (list/create/delete) ----------
    @action(detail=False, methods=["get", "post"], url_path="meal-items")
    def meal_items(self, request):
        if request.method == "GET":
            date_str = request.query_params.get("date")
            qs = MealItem.objects.filter(meal__user=request.user).select_related("meal")
            if date_str:
                d = self._parse_date(date_str)
                qs = qs.filter(meal__date=d)
            qs = qs.order_by("-created_at")[:200]
            return Response({"results": MealItemSerializer(qs, many=True).data})

        # POST
        ser = MealItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        meal = ser.validated_data["meal"]
        self._ensure_owned_meal(meal)
        item = ser.save()
        return Response(MealItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete"], url_path=r"meal-items/(?P<pk>\d+)")
    def meal_item_delete(self, request, pk=None):
        try:
            item = MealItem.objects.select_related("meal").get(pk=pk)
        except MealItem.DoesNotExist:
            raise NotFound("MealItem not found")

        self._ensure_owned_meal(item.meal)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ---------- exercises (list/create/delete) ----------
    @action(detail=False, methods=["get", "post"], url_path="exercises")
    def exercises(self, request):
        if request.method == "GET":
            date_str = request.query_params.get("date")
            qs = ExerciseRecord.objects.filter(user=request.user)
            if date_str:
                d = self._parse_date(date_str)
                qs = qs.filter(date=d)
            qs = qs.order_by("-date", "-id")[:200]
            return Response(
                {
                    "results": ExerciseSerializer(
                        qs, many=True, context={"request": request}
                    ).data
                }
            )

        ser = ExerciseSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        obj = ser.save()  # create()에서 user/estimated_kcal 처리
        return Response(
            ExerciseSerializer(obj, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["delete"], url_path=r"exercises/(?P<pk>\d+)")
    def exercise_delete(self, request, pk=None):
        try:
            obj = ExerciseRecord.objects.get(pk=pk, user=request.user)
        except ExerciseRecord.DoesNotExist:
            raise NotFound("Exercise not found")

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ---------- weight / condition / supplement upsert ----------
    @action(
        detail=False,
        methods=["put"],
        url_path=r"weights/(?P<date_str>\d{4}-\d{2}-\d{2})",
    )
    def weight_upsert(self, request, date_str=None):
        d = self._parse_date(date_str)
        weight_kg = request.data.get("weight_kg")
        if weight_kg is None:
            return Response({"detail": "weight_kg가 필요합니다."}, status=400)

        obj, _ = WeightRecord.objects.update_or_create(
            user=request.user, date=d, defaults={"weight_kg": weight_kg}
        )
        return Response(WeightSerializer(obj).data, status=200)

    @action(
        detail=False,
        methods=["put"],
        url_path=r"conditions/(?P<date_str>\d{4}-\d{2}-\d{2})",
    )
    def condition_upsert(self, request, date_str=None):
        d = self._parse_date(date_str)
        mood = request.data.get("mood")
        if not mood:
            return Response({"detail": "mood가 필요합니다."}, status=400)

        obj, _ = ConditionRecord.objects.update_or_create(
            user=request.user, date=d, defaults={"mood": mood}
        )
        return Response(ConditionSerializer(obj).data, status=200)

    @action(
        detail=False,
        methods=["put"],
        url_path=r"supplements/(?P<date_str>\d{4}-\d{2}-\d{2})",
    )
    def supplement_upsert(self, request, date_str=None):
        d = self._parse_date(date_str)
        taken = bool(request.data.get("taken"))

        obj, _ = SupplementIntake.objects.update_or_create(
            user=request.user, date=d, defaults={"taken": taken}
        )
        return Response(SupplementSerializer(obj).data, status=200)
