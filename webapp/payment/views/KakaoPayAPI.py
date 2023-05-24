import os

import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart


class KakaoPayAPI(APIView):

    def post(self, request, survey_id):
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
            'approval_url': 'http://localhost',
            'fail_url': 'http://localhost',
            'cancel_url': 'http://localhost',
        }
        response = requests.post(url, headers=headers, params=params)
        # if response.status_code == 200:
        #     survey = Survey.objects.get(id=survey_id)
        #     survey.is_paid = True
        #     survey.save()
        result = response.json()
        return Response(result)
