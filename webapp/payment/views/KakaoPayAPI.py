import os

import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from survey.models import Survey

BASEURL = settings.BACKEND_URL

class KakaoPayAPI(APIView):

    def post(self, request, survey_id):
        """
        카카오페이 결제 API를 호출합니다.
        종료된 설문만 결제가 가능합니다.
        """
        survey = Survey.objects.get(id=survey_id)
        if survey.end_at is None:
            return Response({'error': '설문 종료 일시가 설정되지 않았습니다.'}, status=400)
        carts = Cart.objects.filter(survey_id=survey_id)
        total_amount = 0
        for cart in carts:
            total_amount += cart.total_price
        KAKAO_ADMIN_KEY = os.environ.get('KAKAO_ADMIN_KEY')
        url = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            'Authorization': f'KakaoAK {KAKAO_ADMIN_KEY}',
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        # TODO: params url 변경해야함.
        params = {
            'cid': "TC0ONETIME",
            'partner_order_id': '1001',
            'partner_user_id': 'IbelieveSurvey',
            'item_name': '아빌립서베이 기프티콘 결제',
            'quantity': 1,
            'total_amount': total_amount,
            'tax_free_amount': 0,
            'approval_url': f'{BASEURL}surveys/{survey_id}/carts/payments/success',
            'fail_url': f'{BASEURL}',
            'cancel_url': f'{BASEURL}',
        }
        response = requests.post(url, headers=headers, params=params)
        result = response.json()
        return Response(result)
