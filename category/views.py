from django.db.models import Count
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Category
from .serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
    CategoryListSerializer
)


class CategoryView(APIView):
    # 관리자 계정만 열람 및 작성가능
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        주류 카테고리 페이지
        """
        category = Category.objects
        serializer = CategoryListSerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        주류 추가 페이지
        """
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "게시글 작성완료!"})
