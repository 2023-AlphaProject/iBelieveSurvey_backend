from rest_framework import serializers

from user.models import User


class UpdateUserSerializer(serializers.ModelSerializer):
    hidden_realName = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('kakaoId', 'email', 'realName', 'hidden_realName', 'phoneNumber', 'gender', 'birthyear')
        read_only_fields = ('kakaoId', 'email')

    def get_hidden_realName(self, obj):
        return obj.hidden_realName


class UserViewSerializer(serializers.ModelSerializer):
    hidden_realName = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('kakaoId', 'email', 'realName', 'hidden_realName', 'phoneNumber', 'gender', 'birthyear')

    def get_hidden_realName(self, obj):
        return obj.hidden_realName
