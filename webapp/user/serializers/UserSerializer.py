from rest_framework import serializers

from user.models import User

# Serializer for User Update
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('kakaoId', 'email', 'realName', 'phoneNumber', 'gender', 'birth')
        read_only_fields = ('kakaoId', 'email')

# Serializer for User Details
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('kakaoId', 'email', 'realName', 'phoneNumber', 'gender', 'birth')