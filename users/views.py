from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from .tokens import account_activation_token


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """
        마이 페이지
        """
        return Response({"message": "get!"})

    def put(self, request, user_id):
        """
        프로필 수정
        """
        return Response({"message": "put!"})

    def delete(self, request, user_id):
        """
        회원 탈퇴
        """
        return


class FollowingView(APIView):
    def get(self, request, user_id):
        """
        user가 팔로잉하고 있는 목록 보여주기
        """
        return Response({"message": "put!"})


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        print("activate")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, token):
                User.objects.filter(pk=uid).update(is_active=True)
                return Response({"인증 완료!"})
            return Response({"error": "AUTH_FAIL"}, status=400)
        except KeyError:
            return Response({"error": "KEY_ERROR"}, status=400)
