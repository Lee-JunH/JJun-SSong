import calendar
from datetime import date as date_cls
from django.utils.dateparse import parse_date
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import DayRecord, MealItem, ExerciseItem, WeightEntry, ConditionEntry
from .serializers import DaySummarySerializer, DayDetailSerializer, MealItemSerializer, ExerciseItemSerializer

def get_or_create_day(user, d: date_cls) -> DayRecord:
    day, _ = DayRecord.objects.get_or_create(user=user, date=d)
    return day

class CalendarMonthView(APIView):
    """
    GET /api/calendar?month=YYYY-MM
    """
    def get(self, request):
        month_str = request.query_params.get("month")
        if not month_str or len(month_str) != 7:
            return Response({"detail": "month=YYYY-MM is required"}, status=400)

        y = int(month_str[:4])
        m = int(month_str[5:7])
        last_day = calendar.monthrange(y, m)[1]

        start = date_cls(y, m, 1)
        end = date_cls(y, m, last_day)

        qs = DayRecord.objects.filter(user=request.user, date__range=(start, end)).order_by("date")
        data = DaySummarySerializer(qs, many=True).data
        return Response({"month": month_str, "days": data})

class DayDetailView(APIView):
    """
    GET /api/days/YYYY-MM-DD
    """
    def get(self, request, day_str):
        d = parse_date(day_str)
        if not d:
            return Response({"detail": "Invalid date"}, status=400)
        day = get_or_create_day(request.user, d)
        return Response(DayDetailSerializer(day).data)

class AddMealView(APIView):
    """
    POST /api/days/YYYY-MM-DD/meals
    body: { meal_type, name, grams, kcal, carb, protein, fat, sugar, sodium }
    """
    def post(self, request, day_str):
        d = parse_date(day_str)
        if not d:
            return Response({"detail": "Invalid date"}, status=400)
        day = get_or_create_day(request.user, d)

        ser = MealItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        item = MealItem.objects.create(day=day, **ser.validated_data)
        # 요약은 signal로 자동 재계산
        return Response(MealItemSerializer(item).data, status=status.HTTP_201_CREATED)

class DeleteMealView(APIView):
    def delete(self, request, meal_id):
        try:
            item = MealItem.objects.select_related("day").get(id=meal_id, day__user=request.user)
        except MealItem.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)
        item.delete()
        return Response(status=204)

class AddExerciseView(APIView):
    """
    POST /api/days/YYYY-MM-DD/exercises
    """
    def post(self, request, day_str):
        d = parse_date(day_str)
        if not d:
            return Response({"detail": "Invalid date"}, status=400)
        day = get_or_create_day(request.user, d)
        ser = ExerciseItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ex = ExerciseItem.objects.create(day=day, **ser.validated_data)
        return Response(ExerciseItemSerializer(ex).data, status=201)

class UpsertWeightView(APIView):
    """
    PUT /api/days/YYYY-MM-DD/weight  body: { weight_kg }
    """
    def put(self, request, day_str):
        d = parse_date(day_str)
        if not d:
            return Response({"detail": "Invalid date"}, status=400)
        day = get_or_create_day(request.user, d)
        w = request.data.get("weight_kg")
        if w is None:
            return Response({"detail": "weight_kg required"}, status=400)

        obj, _ = WeightEntry.objects.update_or_create(day=day, defaults={"weight_kg": float(w)})
        return Response({"weight_kg": obj.weight_kg})

class UpsertConditionView(APIView):
    """
    PUT /api/days/YYYY-MM-DD/condition body: { emoji, note }
    """
    def put(self, request, day_str):
        d = parse_date(day_str)
        if not d:
            return Response({"detail": "Invalid date"}, status=400)
        day = get_or_create_day(request.user, d)

        emoji = request.data.get("emoji", "")
        note = request.data.get("note", "")
        obj, _ = ConditionEntry.objects.update_or_create(day=day, defaults={"emoji": emoji, "note": note})
        day.condition_emoji = emoji
        day.save(update_fields=["condition_emoji"])
        return Response({"emoji": obj.emoji, "note": obj.note})

class UpdateMealTogglesView(APIView):
    """
    PATCH /api/days/YYYY-MM-DD/toggles
    body: {"breakfast": true} / {"lunch": false} / {"dinner": true} / {"nutrition": true}
    """
    def patch(self, request, day_str):
        d = parse_date(day_str)
        if not d:
            return Response({"detail": "Invalid date"}, status=400)

        day = get_or_create_day(request.user, d)

        allowed = {"breakfast", "lunch", "dinner", "nutrition"}
        updated = []
        for key in allowed:
            if key in request.data:
                setattr(day, key, bool(request.data[key]))
                updated.append(key)

        if not updated:
            return Response({"detail": "No valid fields"}, status=400)

        day.save(update_fields=updated)

        return Response({
            "date": str(day.date),
            "breakfast": day.breakfast,
            "lunch": day.lunch,
            "dinner": day.dinner,
            "nutrition": day.nutrition,
        })

class ReportAvailableMonthsView(APIView):
    """
    GET /api/reports/available-months/
    - 기록이 '있는' 달만 반환 (열어보기만 해서 생긴 빈 DayRecord는 제외)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        active_qs = (
            DayRecord.objects.filter(user=user)
            .annotate(
                meal_count=Count("meals", distinct=True),
                exercise_count=Count("exercises", distinct=True),
            )
            .filter(
                Q(meal_count__gt=0)
                | Q(exercise_count__gt=0)
                | Q(weight__isnull=False)
                | Q(condition__isnull=False)
                | Q(breakfast=True)
                | Q(lunch=True)
                | Q(dinner=True)
                | Q(nutrition=True)
                | Q(total_kcal__gt=0)
                | Q(total_carb__gt=0)
                | Q(total_protein__gt=0)
                | Q(total_fat__gt=0)
            )
        )

        months = (
            active_qs.annotate(m=TruncMonth("date"))
            .values_list("m", flat=True)
            .distinct()
            .order_by("m")
        )

        result = [m.strftime("%Y-%m") for m in months if m]
        return Response({"months": result})


class MonthlyReportView(APIView):
    """
    GET /api/reports/monthly/?month=YYYY-MM

    반환:
    - days: 해당 월 1일~말일까지 일자별 데이터(없으면 null/0)
    - stats: 요약(이번달 마지막 체중, 지난달 마지막 체중 대비 변화, 기록일수 등)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month_str = request.query_params.get("month")
        if not month_str or len(month_str) != 7:
            return Response({"detail": "month=YYYY-MM is required"}, status=400)

        try:
            y = int(month_str[:4])
            m = int(month_str[5:7])
            last_day = calendar.monthrange(y, m)[1]
        except Exception:
            return Response({"detail": "Invalid month format"}, status=400)

        start = date_cls(y, m, 1)
        end = date_cls(y, m, last_day)

        qs = (
            DayRecord.objects.filter(user=request.user, date__range=(start, end))
            .annotate(
                meal_count=Count("meals", distinct=True),
                exercise_count=Count("exercises", distinct=True),
            )
            .select_related("weight", "condition")
            .order_by("date")
        )

        by_date = {dr.date: dr for dr in qs}

        days = []
        for day_num in range(1, last_day + 1):
            d = date_cls(y, m, day_num)
            dr = by_date.get(d)

            if dr:
                w = dr.weight.weight_kg if hasattr(dr, "weight") else None

                has_record = (
                    (dr.meal_count or 0) > 0
                    or (dr.exercise_count or 0) > 0
                    or w is not None
                    or hasattr(dr, "condition")
                    or dr.breakfast
                    or dr.lunch
                    or dr.dinner
                    or dr.nutrition
                    or (dr.total_kcal or 0) > 0
                    or (dr.total_carb or 0) > 0
                    or (dr.total_protein or 0) > 0
                    or (dr.total_fat or 0) > 0
                )

                days.append(
                    {
                        "date": d.isoformat(),
                        "has_record": bool(has_record),
                        "weight_kg": w,
                        "total_kcal": dr.total_kcal,
                        "total_carb": dr.total_carb,
                        "total_protein": dr.total_protein,
                        "total_fat": dr.total_fat,
                        "total_sugar": dr.total_sugar,
                        "total_sodium": dr.total_sodium,
                    }
                )
            else:
                days.append(
                    {
                        "date": d.isoformat(),
                        "has_record": False,
                        "weight_kg": None,
                        "total_kcal": 0,
                        "total_carb": 0,
                        "total_protein": 0,
                        "total_fat": 0,
                        "total_sugar": 0,
                        "total_sodium": 0,
                    }
                )

        recorded_days = sum(1 for x in days if x["has_record"])

        # 이번달 마지막 체중
        current_weight = None
        start_weight_in_month = None
        for x in days:
            if x["weight_kg"] is not None:
                start_weight_in_month = x["weight_kg"]
                break
        for x in reversed(days):
            if x["weight_kg"] is not None:
                current_weight = x["weight_kg"]
                break

        # 지난달 마지막 체중
        if m == 1:
            py, pm = y - 1, 12
        else:
            py, pm = y, m - 1
        prev_last_day = calendar.monthrange(py, pm)[1]
        prev_start = date_cls(py, pm, 1)
        prev_end = date_cls(py, pm, prev_last_day)

        prev_last_weight_obj = (
            WeightEntry.objects.filter(
                day__user=request.user,
                day__date__range=(prev_start, prev_end),
            )
            .order_by("day__date")
            .last()
        )
        prev_month_last_weight = (
            prev_last_weight_obj.weight_kg if prev_last_weight_obj else None
        )

        change_from_prev_month = None
        if current_weight is not None and prev_month_last_weight is not None:
            change_from_prev_month = round(current_weight - prev_month_last_weight, 1)

        return Response(
            {
                "month": month_str,
                "days": days,
                "stats": {
                    "recorded_days": recorded_days,
                    "weight": {
                        "start_in_month": start_weight_in_month,
                        "current": current_weight,
                        "prev_month_last": prev_month_last_weight,
                        "change_from_prev_month": change_from_prev_month,
                    },
                },
            }
        )

