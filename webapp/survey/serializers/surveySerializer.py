from rest_framework import serializers

from survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id',
            'title',
            'thumbnail',
            'category',
            'started_at',
            'end_at',
            'is_idle',
            'is_ongoing',
            'is_done',
            'is_awarded',
            'is_survey_hidden',
            'created_at',
            'participants',
        ]

        read_only_fields = [
            'created_at',
            'started_at',
            'data',
            'is_idle',
            'is_awarded',
            'is_ongoing',
            'is_done',
            'participants',
        ]

    def get_participants(self, obj):
        return obj.participant_set.count()
