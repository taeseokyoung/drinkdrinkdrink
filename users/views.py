from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from users.serializers import UserSerializer


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,user_id):
        """
        마이 페이지
        """
        return Response({"message":"get!"})
    
    def put(self, request,user_id):
        """
        프로필 수정
        """
        return Response({"message":"put!"})
    
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
        return Response({"message":"put!"})
    