from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView

from gifticon.models import Gifticon

# 설문조사가 완료되면 "카카오톡 선물하기" 과정 시작
# 기프티콘을 다 고르면 해당 총금액만큼 "카카오페이" 과정 시작
# 해당 총금액을 송금했다면
# 카카오톡 선물하기 완료
IDLE = 0
ONGOING = 1
DONE = 2
AWARDED = 3

class gifticonAPIView(APIView):

    # 해당 설문 status가 IDLE, ONGOING, DONE, AWRARDED인지 판별.
    # 해당 설문 status가 ONGOING이면 기프티콘을 구매할 수 있다.
    def identifySurveyStatus(self, request, pk):
        pass

    # 기프티콘 수 > 참여자 수라면 설문종료시간(end_at) 24시간 증가
    def increaseSurveyEndAt(self, request, pk):
        pass

    # 해당 설문에서 결제된 기프티콘 내역 가져오기
    def getGifticon(self, request, pk):
        pass

    # 해당 설문에서 기프티콘 결제 시작하기
    def postGifticon(self, request):
        pass


