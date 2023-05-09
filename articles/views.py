from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from models import Article
from serializers import ArticleDetailSerializer

class HomeView(APIView):
    def get(self, request):
        """
        HOME
        """
        return Response({"message":"get!"})
    

class ArticleWriteView(APIView):
    def post(self, request):
        """
        게시글 작성 페이지
        """
        return Response({"message":"post!"})
    

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
        return Response({"message":"좋아요 누르기"})


class CommentView(APIView):
    def post(self, request):
        '''댓글 쓰기'''
        return Response({"message":"댓글 작성"})

    def put(self, reuqest, comment_id):
        '''댓글 수정'''
        return Response({"message":"댓글 수정"})

    def delete(self, request, comment_id):
        '''댓글 삭제'''
        return Response({"message": "댓글 삭제"})