from rest_framework.decorators import action
from rest_framework.views import APIView

from config.pagination import DefaultPagination
from survey.models import Survey
from survey.serializers import SurveySerializer


class MyPageViewSet(APIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = DefaultPagination

    @action(detail=False, methods=['GET'])
    def paid(self, request):
        surveys = Survey.objects.filter(writer=request.user, is_paid=True)
        page = self.paginate_queryset(surveys)
        serializer = SurveySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['GET'])
    def participated(self, request):
        surveys = Survey.objects.filter(participants=request.user)
        page = self.paginate_queryset(surveys)
        serializer = SurveySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
