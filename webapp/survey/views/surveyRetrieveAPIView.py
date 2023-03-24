from django.utils import timezone
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response

from survey.models import Survey
from survey.serializers import SurveyRetrieveSerializer


class SurveyRetrieveDestoryAPIView(RetrieveDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyRetrieveSerializer

    # 설문이 비공개 상태이고 종료일이 지났을 경우, data 필드를 제외한 나머지 필드만 반환
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_survey_hidden and instance.end_at < timezone.now():
            serializer = self.get_serializer(instance, exclude_fields=['data'])
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)
