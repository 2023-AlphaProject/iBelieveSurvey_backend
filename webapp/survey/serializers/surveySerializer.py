from rest_framework import serializers

from survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id',
            'writer',
            'title',
            'thumbnail',
            'category',
            'status',
            'is_paid',
            'started_at',
            'end_at',
            'is_survey_hidden',
            'participants',
            'created_at',
        ]

        read_only_fields = [
            'created_at',
            'started_at',
            'data',
            'writer',
            'status',
            'is_paid',
            'participants',
        ]

    def get_participants(self, obj):
        return obj.participant_set.count()
