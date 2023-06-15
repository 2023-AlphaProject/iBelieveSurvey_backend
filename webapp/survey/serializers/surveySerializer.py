from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers
from survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    winningPercentage = serializers.SerializerMethodField()

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
            'participants',
            'created_at',
            'winningPercentage',
        ]

        read_only_fields = [
            'writer',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'participants',
            'created_at',
            'winningPercentage',
        ]

    def get_participants(self, obj):
        try:
            return obj.participant_set.count()
        except AttributeError:
            return 0

    def get_winningPercentage(self, obj):
        return obj.winningPercentage

    def create(self, validated_data):
        thumbnail = validated_data.pop('thumbnail', None)
        survey = Survey.objects.create(**validated_data)  # thumbnail 필드를 제외한 나머지 필드로 Survey 객체 생성

        if thumbnail:
            file_name = default_storage.save(thumbnail.name, ContentFile(thumbnail.read()))
            survey.thumbnail = file_name
            survey.save()

        return survey
