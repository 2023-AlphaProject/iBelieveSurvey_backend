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
            'status',
            'end_at',
            'is_survey_hidden',
            'created_at',
        ]

        read_only_fields = [
            'created_at',
            'data',
        ]
