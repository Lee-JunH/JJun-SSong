from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Food, CustomFood, FoodFavorite
from .serializers import CustomFoodCreateSerializer, FavoriteSerializer

class FoodSearchView(APIView):
    """
    GET /api/foods/search?q=...
    public Food + user CustomFood를 합쳐서 반환
    """
    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        if not q:
            return Response({"items": []})

        foods = Food.objects.filter(name__icontains=q).order_by("name")[:20]
        customs = CustomFood.objects.filter(user=request.user, name__icontains=q).order_by("name")[:20]

        items = []
        for f in foods:
            items.append({
                "source": "public",
                "id": f.id,
                "name": f.name,
                "per_100g_kcal": f.per_100g_kcal,
                "per_100g_carb": f.per_100g_carb,
                "per_100g_protein": f.per_100g_protein,
                "per_100g_fat": f.per_100g_fat,
                "per_100g_sugar": f.per_100g_sugar,
                "per_100g_sodium": f.per_100g_sodium,
            })
        for c in customs:
            items.append({
                "source": "custom",
                "id": c.id,
                "name": c.name,
                "per_100g_kcal": c.per_100g_kcal,
                "per_100g_carb": c.per_100g_carb,
                "per_100g_protein": c.per_100g_protein,
                "per_100g_fat": c.per_100g_fat,
                "per_100g_sugar": c.per_100g_sugar,
                "per_100g_sodium": c.per_100g_sodium,
            })

        return Response({"items": items})

class CustomFoodCreateView(APIView):
    """
    POST /api/foods/custom
    """
    def post(self, request):
        ser = CustomFoodCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save(user=request.user)
        return Response(CustomFoodCreateSerializer(obj).data, status=201)

class FavoritesView(APIView):
    def get(self, request):
        qs = FoodFavorite.objects.filter(user=request.user).order_by("-created_at")[:100]
        return Response(FavoriteSerializer(qs, many=True).data)

    def post(self, request):
        ser = FavoriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = FoodFavorite.objects.create(user=request.user, **ser.validated_data)
        return Response(FavoriteSerializer(obj).data, status=201)

class FavoriteDeleteView(APIView):
    def delete(self, request, fav_id):
        deleted, _ = FoodFavorite.objects.filter(user=request.user, id=fav_id).delete()
        if not deleted:
            return Response({"detail": "Not found"}, status=404)
        return Response(status=204)
