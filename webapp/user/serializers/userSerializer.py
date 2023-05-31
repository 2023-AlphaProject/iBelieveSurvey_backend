from rest_framework import serializers

from user.models import User


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('kakaoId', 'email', 'realName', 'phoneNumber', 'gender', 'birthyear')
        read_only_fields = ('kakaoId', 'email')


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('kakaoId', 'email', 'realName', 'phoneNumber', 'gender', 'birthyear')
