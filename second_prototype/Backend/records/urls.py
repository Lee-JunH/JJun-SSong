from django.urls import path
from .views import (
    CalendarMonthView,
    DayDetailView,
    AddMealView,
    DeleteMealView,
    AddExerciseView,
    UpsertWeightView,
    UpsertConditionView,
    UpdateMealTogglesView,
    # ✅ 추가
    ReportAvailableMonthsView,
    MonthlyReportView,
)

urlpatterns = [
    path("calendar/", CalendarMonthView.as_view()),
    path("days/<str:day_str>/", DayDetailView.as_view()),
    path("days/<str:day_str>/meals/", AddMealView.as_view()),
    path("meals/<int:meal_id>/", DeleteMealView.as_view()),
    path("days/<str:day_str>/exercises/", AddExerciseView.as_view()),
    path("days/<str:day_str>/weight/", UpsertWeightView.as_view()),
    path("days/<str:day_str>/condition/", UpsertConditionView.as_view()),
    path("days/<str:day_str>/toggles/", UpdateMealTogglesView.as_view()),

    # ✅ 리포트 API
    path("reports/available-months/", ReportAvailableMonthsView.as_view()),
    path("reports/monthly/", MonthlyReportView.as_view()),
]
