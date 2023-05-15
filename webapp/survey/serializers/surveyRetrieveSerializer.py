from rest_framework import serializers

from survey.models import Survey


class SurveyRetrieveSerializer(serializers.ModelSerializer):
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
            'data', #
        ]
        read_only_fields = [
            'created_at',
            'is_idle',
            'is_awarded',
            'is_ongoing',
            'is_done',
            'started_at',
        ]
