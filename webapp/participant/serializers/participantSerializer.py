from rest_framework import serializers

from participant.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    json_quality_standard = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = [
            'id',
            'user',
            'survey',
            'json',
            'created_at',
            'update_at',
            'json_quality_standard',
        ]

        read_only_fields = [
            'created_at',
            'update_at',
            'json_quality_standard',
        ]

    def get_json_quality_standard(self, obj):
        return obj.json_quality_standard
