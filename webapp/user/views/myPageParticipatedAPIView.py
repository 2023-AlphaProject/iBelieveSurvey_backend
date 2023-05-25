from rest_framework.views import APIView

from config.pagination import DefaultPagination
from participant.models import Participant
from survey.models import Survey
from survey.serializers import SurveySerializer


class MyPageParticipatedAPIView(APIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = DefaultPagination

    def get(self, request):
        """
        자신이 참여한 설문들을 반환합니다.
        """
        participants = Participant.objects.filter(user=request.user)
        surveys = []
        for participant in participants:
            surveys.append(participant.survey)
        paginator = self.pagination_class()
        paginated_surveys = paginator.paginate_queryset(surveys, request)
        serializer = self.serializer_class(paginated_surveys, many=True)
        return paginator.get_paginated_response(serializer.data)
