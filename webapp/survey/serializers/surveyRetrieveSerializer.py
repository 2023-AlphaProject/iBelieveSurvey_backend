from rest_framework import serializers

from survey.models import Survey


class SurveyListSerializer(serializers.ModelSerializer):
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
