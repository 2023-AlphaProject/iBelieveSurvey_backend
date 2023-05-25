from django.shortcuts import redirect
from rest_framework.views import APIView

from survey.models import Survey


class KakaoPaySuccess(APIView):
    def get(self, request, survey_id):
        survey = Survey.objects.get(id=survey_id)
        survey.is_paid = True
        survey.save()
        return redirect('http://localhost')
