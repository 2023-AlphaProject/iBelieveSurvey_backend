from rest_framework.response import Response
from rest_framework.views import APIView

from survey.models import Survey
from survey.serializers.survey_serializer import SurveySerializer


class SurveyListApiView(APIView):
    def get(self, request, format=None):
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data)
