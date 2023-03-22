# Create your views here.
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Survey
from .serializers import SurveySerializer


# Create your views here.
class ListSurveyView(APIView):
    def get(self, request, format=None):
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data)
