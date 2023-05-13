from rest_framework.generics import CreateAPIView, ListAPIView

from survey.models import Survey
from survey.serializers import SurveySerializer


class SurveyAPIView(CreateAPIView, ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    # TODO: filter, permission, pagination
