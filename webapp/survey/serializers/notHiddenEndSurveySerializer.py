from rest_framework import serializers

from survey.models import Survey


class NotHiddenEndSurveySerializer(serializers.ModelSerializer):
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
            'data',
            'is_survey_hidden',
            'participants',
            'created_at',
        ]
        read_only_fields = [
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
            'data',
            'is_survey_hidden',
            'participants',
            'created_at',
        ]

    def get_participants(self, obj):
        try:
            return obj.participant_set.count()
        except AttributeError:
            return 0
