from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    # UserSerializer 있다고 가정
    # user = User

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
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    # comment 불러오는 건 comment 시리얼라이저 만들어지면 수정!
    # comments = 코멘트시리얼라이저(many=True)

    likes_num = serializers.SerializerMethodField()

    # user를 user_id로 보여줌
    def get_user(self, obj):
        return obj.user.identify

    # 현재 게시글의 좋아요 갯수 들고오기
    def get_likes_num(self, obj):
        return obj.likes.count()

    class Meta:
        model = Article
        fields = "__all__"
