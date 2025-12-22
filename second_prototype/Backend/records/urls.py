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
]
