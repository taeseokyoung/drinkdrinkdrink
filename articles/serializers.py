from rest_framework import serializers
from .models import Article

class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # comment 불러오는 건 comment 시리얼라이저 만들어지면 수정!
    # comments = 코멘트시리얼라이저(many=True)
    likes = serializers.StringRelatedField(many=True)

    
    # user를 user_id로 보여줌
    def get_user(self, obj):
        return obj.user.user_id
    
    class Meta:
        model = Article
        fields = '__all__'