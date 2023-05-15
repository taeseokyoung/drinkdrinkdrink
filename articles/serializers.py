from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        exclude = ("article", "created_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class ArticleListSerializer(serializers.ModelSerializer):
    # user,like = something.serializer
    
    # 페이지에 총 좋아요 수를 불러올 수 있다.
    total_likes = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = (
            "id",
            "user",
            "title",
            "content",
            "image",
            "likes",
            "total_likes",
            "stars",
            "created_at",
            "updated_at",
        )

    def get_total_likes(self,article):
        return article.total_likes()


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "content", "stars", "image")  # user는 제외!


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    nickname = serializers.SerializerMethodField()
    likes_num = serializers.SerializerMethodField()

    # 현재 게시글의 좋아요 갯수 들고오기
    def get_likes_num(self, obj):
        return obj.likes.count()
    
    # 현재 게시글의 유저 닉네임 들고오기
    def get_nickname(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        fields = "__all__"
