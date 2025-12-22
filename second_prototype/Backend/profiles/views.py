from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer


class MyProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # 프로필이 없으면 자동 생성 → 프론트가 404 처리할 필요 없음
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
