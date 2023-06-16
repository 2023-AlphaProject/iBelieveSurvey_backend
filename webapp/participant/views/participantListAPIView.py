from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from participant.models import Participant
from participant.serializers.participantSerializer import ParticipantSerializer
from survey.models import Survey


class JsonQualityStandardOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            # Check if the first ordering field is 'json_quality_standard'
            if ordering[0] == 'json_quality_standard':
                is_descending = ordering[0].startswith('-')
                return sorted(queryset, key=lambda p: p.json_quality_standard, reverse=is_descending)

        return queryset


class ParticipantListAPIView(ListCreateAPIView):
    serializer_class = ParticipantSerializer
    ordering = ['id']
    filter_backends = [JsonQualityStandardOrderingFilter]
    ordering_fields = ['json_quality_standard']

    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        queryset = Participant.objects.filter(survey_id=survey_id).order_by('id')

        return queryset

    def get(self, request, *args, **kwargs):
        """
        설문 작성자가 해당 설문에 대한 모든 답변들을 조회합니다.
        """
        if not request.user:
            return Response({"error": "해당 설문에 대한 답변들을 조회하기 위해선 로그인이 필요합니다."})

        if self.request.user != self.get_survey().writer:
            return Response({"error": "설문 작성자 본인만이 해당 설문에 대한 답변들을 조회할 수 있습니다."})

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        설문 참여자가 해당 설문에 대한 답변을 생성합니다.
        """
        if not request.user:
            return Response({"error": "설문에 답변하기 위해선 로그인이 필요합니다."})

        if self.request.user != self.get_survey().writer:
            return Response({"error": "설문 작성자는 본인의 설문에 답변할 수 없습니다."})

        if not self.get_survey().is_ongoing:
            return Response({"error": "설문이 진행 중이 아니므로 답변할 수 없습니다."})

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        survey = self.get_survey()
        serializer.save(survey=survey, user=self.request.user)

    def get_survey(self):
        survey_id = self.kwargs['survey_id']
        survey = Survey.objects.get(id=survey_id)
        return survey
