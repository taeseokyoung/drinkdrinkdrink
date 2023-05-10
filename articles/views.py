from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Article
from .serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
)


# page?=1,2,3...
class HomeView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        order_condition = request.query_params.get("order", None)
        if order_condition == "recent":
            articles = Article.objects.order_by("created_at")
        if order_condition == "likes":
            articles = Article.objects.order_by("likes")
        if order_condition == "stars":
            articles = Article.objects.order_by("stars")
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        serializer = ArticleListSerializer(
            articles[start:end],
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleWriteView(APIView):
    def post(self, request):
        """
        게시글 작성 페이지
        """
        return Response({"message": "post!"})


class ArticleDetailView(APIView):
    def get(self, request, article_id):
        """
        상세 게시글 보기 / 댓글 띄우기
        """

        # 게시글 id로 게시글 존재 여부 확인
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        """
        상세 게시글 수정
        """

        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            # 게시글 작성하는 시리얼라이저랑 같은 시리얼라이저 사용
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("게시글 수정 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        """
        상세 게시글 삭제
        """

        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response("게시글이 삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("게시글 삭제 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView):
    def post(self, request):
        """한 번 누르면 좋아요.
        두 번 누르면 좋아요를 취소합니다."""
        return Response({"message": "좋아요 누르기"})


# comment 클래스 추가
class CommentView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(pk=article_id)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user, article=Article.objects.get(pk=article_id)
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = Article.objects.get(pk=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Article, pk=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제완료", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
