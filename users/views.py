from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404

from .models import User
from .serializers import UserSerializer, UserProfileSerializer, UserProfileEditSerializer
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
    # 비로그인 유저도 프로필까지는 볼 수 있음 permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """
        마이 페이지
        """
        user = get_object_or_404(User,id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, user_id):
        """
        프로필 수정
        """
        # serializer = UserSerializer(data=request.data)
        # myInfo = User.objects.get(id=user_id)
        user = get_object_or_404(User,id=user_id)
        serializer = UserProfileEditSerializer(user, data=request.data)
        # print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
 
        
    def delete(self, request, user_id):
        """
        회원 탈퇴
        """
        return


class FollowView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User,id=user_id)
        user.is_active=False
        user.save()
        return Response({'message':'delete 요청!'})      
                  
class FollowingView(APIView):
    def get(self, request, user_id):
        """
        현재 페이지의 유저(user_id)를 follow 하기
        """
        # you : 현재 페이지 번호의 user, me : 로그인 된 유저(나)
        you = get_object_or_404(User, id=user_id)
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
