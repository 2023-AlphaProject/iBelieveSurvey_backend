from rest_framework import serializers

from survey.models import Survey, Category


class SurveyRetrieveSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    winningPercentage = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id',
            'writer',
            'title',
            'outline',
            'thumbnail',
            'basic_thumbnail',
            'category',
            'category_name',
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
            'winningPercentage',
        ]
        read_only_fields = [
            'writer',
            'is_idle',
            'is_paid',
            'is_ongoing',
            'is_end',
            'started_at',
            'created_at',
            'category_name',
            'participants',
            'winningPercentage',
        ]

    def get_participants(self, obj):
        try:
            return obj.participant_set.count()
        except AttributeError:
            return 0

    def get_winningPercentage(self, obj):
        return obj.winningPercentage

    def get_category_name(self, obj):
        return obj.category.type