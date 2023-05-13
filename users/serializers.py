from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import serializers

from .models import User
from .tokens import account_activation_token
from articles.serializers import ArticleListSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = "__all__"
        extra_kwargs = {
            "followings": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # serializer에서 domain받아 올 방법 찾기
        # current_site = get_current_site(validated_data)
        # domain = current_site.domain

        # url에 포함될 user.id 에러 방지용  encoding하기
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        # tokens.py에서 함수 호출
        token = account_activation_token.make_token(user)
        to_email = user.email
        email = EmailMessage(
            "AOA 술술술 이메일 인증",
            f"http://127.0.0.1:8000/users/activate/{uidb64}/{token}",
            to=[to_email],
        )
        email.send()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    # followings = serializers.StringRelatedField(many=True) user_id로 설정하고 싶을 때 사용
    # related_name 으로 설정함
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    my_articles = ArticleListSerializer(many=True)
    # 라이크 아티클인데.. 팔로우를 한 사람의 피드가 보여지는 것 같아요...?
    like_articles = ArticleListSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "user_id", "nickname", "profile_img", "password",
                  "fav_alcohol", "amo_alcohol", "followings","followers","like_articles", "my_articles")
        
        # "followers", "my_articles","like_articles"


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id","nickname","profile_img","fav_alcohol", "amo_alcohol","password"]
        extra_kwargs = {
            "user_id": {
                "read_only": True,
            },

            "password":{
                "write_only": True,
            },
        }

    # instance = database
    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)
        instance.fav_alcohol = validated_data.get('fav_alcohol', instance.fav_alcohol)
        instance.amo_alcohol = validated_data.get('amo_alcohol', instance.amo_alcohol)
        password = validated_data.pop("password")
        instance.set_password(password) # 해싱
        instance.save() # 데이터베이스에 저장
        return instance





    
    
    