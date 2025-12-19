from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, EmailTokenObtainPairView, MeView, ProfileUpdateView

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/token/", EmailTokenObtainPairView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
    path("me/profile/", ProfileUpdateView.as_view()),
]
