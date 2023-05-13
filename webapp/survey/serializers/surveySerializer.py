from rest_framework import serializers

from survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):
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
        ]

        read_only_fields = [
            'created_at',
            'started_at',
            'data',
            'is_idle',
            'is_awarded',
            'is_ongoing',
            'is_done',
        ]
