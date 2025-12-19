from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Food, CustomFood
from .serializers import FoodSerializer, CustomFoodSerializer


class FoodSearchView(APIView):
    """
    GET /api/foods/search/?q=...
    - dataset Food + 내 CustomFood를 합쳐서 반환
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        if not q:
            return Response({"results": []})

        foods = Food.objects.filter(name__icontains=q).order_by("name")[:20]
        custom = CustomFood.objects.filter(
            owner=request.user, name__icontains=q
        ).order_by("name")[:20]

        results = (
            FoodSerializer(foods, many=True).data
            + CustomFoodSerializer(custom, many=True).data
        )
        return Response({"results": results})


class CustomFoodViewSet(viewsets.ModelViewSet):
    serializer_class = CustomFoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomFood.objects.filter(owner=self.request.user).order_by(
            "-created_at"
        )

    def get_serializer_context(self):
        return {"request": self.request}
