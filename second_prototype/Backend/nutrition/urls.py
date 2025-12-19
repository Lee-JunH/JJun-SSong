from django.urls import path
from .views import FoodSearchView, CustomFoodCreateView, FavoritesView, FavoriteDeleteView

urlpatterns = [
    path("foods/search/", FoodSearchView.as_view()),
    path("foods/custom/", CustomFoodCreateView.as_view()),
    path("foods/favorites/", FavoritesView.as_view()),
    path("foods/favorites/<int:fav_id>/", FavoriteDeleteView.as_view()),
]
