from rest_framework import serializers

from user.models import User

# Serializer for User Update
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('realName', 'phoneNumber', 'gender', 'birth')

# Serializer for User Details
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('kakaoId', 'email', 'realName', 'phoneNumber', 'gender', 'birth')