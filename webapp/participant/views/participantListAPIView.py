from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from survey.models import Survey
from participant.models import Participant
from participant.permissions.participantPermission import ParticipantPermission
from participant.serializers.participantSerializer import ParticipantSerializer


class JsonQualityStandardOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            # Check if the first ordering field is 'json_quality_standard'
            if ordering[0] == 'json_quality_standard':
                is_descending = ordering[0].startswith('-')
                return sorted(queryset, key=lambda p: p.json_quality_standard, reverse=is_descending)

        return queryset


class ParticipantListAPIView(ListAPIView):
    serializer_class = ParticipantSerializer
    ordering = ['id']
    queryset = Participant.objects.all()
    filter_backends = [JsonQualityStandardOrderingFilter]
    ordering_fields = ['json_quality_standard']

    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        queryset = Participant.objects.filter(survey_id=survey_id).order_by('id')

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error": "설문에 답변하기 위해선 로그인이 필요합니다."})

        if self.request.user == self.get_survey_writer():
            return Response({"error": "설문 작성자는 본인의 설문에 답변할 수 없습니다."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def get_survey_writer(self):
        survey_id = self.kwargs['survey_id']
        survey = Survey.objects.get(id=survey_id)
        return survey.writer
