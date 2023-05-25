from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.views import APIView

from survey.models import Survey


class KakaoPaySuccess(APIView):
    def get(self, request, survey_id):
        survey = Survey.objects.get(id=survey_id)
        survey.is_idle = False
        survey.is_paid = True
        survey.started_at = timezone.now()
        survey.save()
        return redirect('http://localhost')
