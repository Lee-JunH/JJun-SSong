import calendar
from datetime import date as date_cls
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
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

