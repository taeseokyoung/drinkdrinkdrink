from rest_framework.views import APIView
from rest_framework.response import Response


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
        return Response({"message":"get!"})
    
    def put(self, request, article_id):
        """
        상세 게시글 수정
        """
        return Response({"message":"put!"})
    
    def delete(self, request, article_id):
        """
        상세 게시글 삭제
        """
        return Response({"message":"delete!"})
    

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