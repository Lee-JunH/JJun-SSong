from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Food, CustomFood, FoodFavorite
from .serializers import CustomFoodCreateSerializer, FavoriteSerializer


class FoodSearchView(APIView):
    """GET /api/foods/search?q=...

    - 공용 Food + (로그인 시) CustomFood를 합쳐서 반환
    """

    permission_classes = [AllowAny]

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        if not q:
            return Response({"items": []})

        foods = Food.objects.filter(name__icontains=q).order_by("name")[:20]

        customs = CustomFood.objects.none()
        if request.user.is_authenticated:
            customs = CustomFood.objects.filter(
                user=request.user, name__icontains=q
            ).order_by("name")[:20]

        items = []
        for f in foods:
            items.append(
                {
                    "source": "public",
                    "id": f.id,
                    "name": f.name,
                    "energy_kcal": f.energy_kcal,
                    "carbs_g": f.carbs_g,
                    "protein_g": f.protein_g,
                    "fat_g": f.fat_g,
                    "sugars_g": f.sugars_g,
                    "sodium_mg": f.sodium_mg,
                }
            )

        for c in customs:
            items.append(
                {
                    "source": "custom",
                    "id": c.id,
                    "name": c.name,
                    "energy_kcal": c.energy_kcal,
                    "carbs_g": c.carbs_g,
                    "protein_g": c.protein_g,
                    "fat_g": c.fat_g,
                    "sugars_g": c.sugars_g,
                    "sodium_mg": c.sodium_mg,
                }
            )

        return Response({"items": items})


class CustomFoodCreateView(APIView):
    """POST /api/foods/custom

    Body:
      { name, energy_kcal, carbs_g, protein_g, fat_g, sugars_g, sodium_mg }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = CustomFoodCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save(user=request.user)
        return Response(CustomFoodCreateSerializer(obj).data, status=201)


class FavoritesView(APIView):
    """GET/POST /api/foods/favorites

    - 즐겨찾기는 '스냅샷 저장' 방식이라, 프론트에서 선택된 음식의 현재 영양값을 그대로 전송해 저장합니다.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = FoodFavorite.objects.filter(user=request.user).order_by("-created_at")[
            :100
        ]
        return Response(FavoriteSerializer(qs, many=True).data)

    def post(self, request):
        ser = FavoriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = FoodFavorite.objects.create(user=request.user, **ser.validated_data)
        return Response(FavoriteSerializer(obj).data, status=201)


class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, fav_id):
        deleted, _ = FoodFavorite.objects.filter(user=request.user, id=fav_id).delete()
        if not deleted:
            return Response({"detail": "Not found"}, status=404)
        return Response(status=204)
