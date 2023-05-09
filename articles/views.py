from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Article
from .serializers import CommentCreateSerializer, CommentSerializer


class HomeView(APIView):
    def get(self, request):
        """
        HOME
        """
        return Response({"message": "get!"})


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
        return Response({"message": "get!"})

    def put(self, request, article_id):
        """
        상세 게시글 수정
        """
        return Response({"message": "put!"})

    def delete(self, request, article_id):
        """
        상세 게시글 삭제
        """
        return Response({"message": "delete!"})


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
