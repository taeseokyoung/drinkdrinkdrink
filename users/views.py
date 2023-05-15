from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import User
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserProfileEditSerializer,
)
from .tokens import account_activation_token


class UserView(APIView):
    def post(self, request):
        if request.data["password_check"] != request.data["password"]:
            return Response(
                {"message": "비밀번호 불일치!"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, token):
                User.objects.filter(pk=uid).update(is_active=True)
                return redirect("http://127.0.0.1:5500/doc/login.html")
            return Response({"error": "AUTH_FAIL"}, status=400)
        except KeyError:
            return Response({"error": "KEY_ERROR"}, status=400)


class ProfileView(APIView):
    def get(self, request, id):
        """
        마이 페이지
        """

        user = get_object_or_404(User,id=id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, id):
        """
        프로필 수정
        """
        
        user = get_object_or_404(User,id=id)
        if request.user.id == user.id:
            serializer = UserProfileEditSerializer(user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message":"본인만 수정할 수 있습니다."} , status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, id):
        """
        회원 탈퇴
        """
        user = get_object_or_404(User,id=id)
        if request.user.id == user.id:
            user = request.user
            user.is_active = False
            user.save()
            return Response({"message":"탈퇴하였습니다."})
        else:
            return Response(
                {"message":"본인만 신청할 수 있습니다."} , status=status.HTTP_401_UNAUTHORIZED)
        # user = request.user
        # user.is_active = False
        # user.save()
        # return
                                 
class FollowView(APIView):
    def get(self, request, id):
        """
        현재 페이지의 유저(id)를 follow 하기
        """
        # you : 현재 페이지 번호의 user, me : 로그인 된 유저(나)
        you = get_object_or_404(User, id=id)
        me = request.user
        # 만약 you의 팔로워 목록에 me가 있으면
        if me in you.followers.all():
            # 팔로우 취소
            you.followers.remove(me)
            return Response("팔로우를 취소했습니다.", status=status.HTTP_200_OK)
        # you의 팔로워 목록에 me가 없으면
        else:
            # 팔로우 하기
            you.followers.add(me)
            return Response("팔로우 했습니다.", status=status.HTTP_200_OK)
