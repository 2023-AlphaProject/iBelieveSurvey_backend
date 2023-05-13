from rest_framework import serializers

from survey.models import Survey


class SurveyRetrieveSerializer(serializers.ModelSerializer):
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
            'data',
            'participants',
        ]
        read_only_fields = [
            'created_at',
            'is_idle',
            'is_awarded',
            'is_ongoing',
            'is_done',
            'started_at',
            'participants',
        ]

    def get_participants(self, obj):
        return obj.participant_set.count()
