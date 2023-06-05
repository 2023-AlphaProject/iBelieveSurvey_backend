from rest_framework import serializers
from user.models import User


class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'hidden_realName',
            'hidden_phoneNumber',
        ]
