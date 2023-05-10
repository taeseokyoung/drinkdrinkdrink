from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import serializers

from .models import User
from .tokens import account_activation_token


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
