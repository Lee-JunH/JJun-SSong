from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodSearchView, CustomFoodViewSet

router = DefaultRouter()
router.register("custom-foods", CustomFoodViewSet, basename="custom-foods")

urlpatterns = [
    path("foods/search/", FoodSearchView.as_view()),
    path("", include(router.urls)),
]
