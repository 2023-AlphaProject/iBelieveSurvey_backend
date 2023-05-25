from rest_framework import serializers

from survey.models import Survey


class SurveyRetrieveSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id',
            'writer',
            'title',
            'thumbnail',
            'category',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'end_at',
            'is_survey_hidden',
            'data',
            'participants',
            'created_at',
        ]
        read_only_fields = [
            'writer',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'end_at',
            'created_at',
            'participants',
        ]

    def get_participants(self, obj):
        return obj.participant_set.count()
