from rest_framework import serializers

from participant.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            'user',
            'survey',
            'json',
            'created_at',
            'update_at',
        ]
        read_only_fields = [
            'created_at',
            'update_at',
        ]
