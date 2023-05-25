from rest_framework.views import APIView

from config.pagination import DefaultPagination
from survey.models import Survey
from survey.serializers import SurveySerializer


class MyPagePaidAPIView(APIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = DefaultPagination

    def get(self, request):
        """
        자신이 결제한 설문들을 반환합니다.
        """
        surveys = Survey.objects.filter(writer=request.user, is_paid=True)
        paginator = self.pagination_class()
        paginated_surveys = paginator.paginate_queryset(surveys, request)
        serializer = self.serializer_class(paginated_surveys, many=True)
        return paginator.get_paginated_response(serializer.data)
