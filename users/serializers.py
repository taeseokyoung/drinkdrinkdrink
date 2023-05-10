from rest_framework import serializers
from .models import User
from django.core.mail import EmailMessage


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

        to_email = user.email
        email = EmailMessage("title", "content", to=[to_email])
        email.send()
        return user
