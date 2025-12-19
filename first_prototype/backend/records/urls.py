from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecordsHubViewSet

router = DefaultRouter()
router.register("records", RecordsHubViewSet, basename="records")

urlpatterns = [
    path("", include(router.urls)),
]
