from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    RegisterSerializer,
    MeSerializer,
    ChangePasswordSerializer,
    DeleteAccountSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(MeSerializer(user).data, status=status.HTTP_201_CREATED)


class MeView(APIView):
    def get(self, request):
        return Response(MeSerializer(request.user).data)

    def patch(self, request):
        ser = MeSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class MeView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ 권장: 명시

    def get(self, request):
        return Response(MeSerializer(request.user).data)

    def patch(self, request):
        ser = MeSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = ChangePasswordSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)

        request.user.set_password(ser.validated_data["new_password1"])
        request.user.save(update_fields=["password"])

        # 보안/UX 측면에서 프론트는 성공 후 로그아웃 처리 권장
        return Response(
            {"detail": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK
        )


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = DeleteAccountSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)

        user = request.user
        user.delete()  # ✅ 연관 FK/OneToOne이 CASCADE면 함께 삭제됨
        return Response(status=status.HTTP_204_NO_CONTENT)
