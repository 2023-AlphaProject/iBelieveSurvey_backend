import requests
from order.models import Order
from participant.models import Participant
from rest_framework.response import Response
from rest_framework.views import APIView

class OrderAPIView(APIView):

    def send_gift_API(self, request, ):


        url = "https://gateway-giftbiz.kakao.com/openapi/giftbiz/v1/template/order"

        payload = {
            "receiver_type": "PHONE",
            "receivers": [{"receiver_id": "010-0000-0000"}],
            "template_token": "Nm1xMWpGQlhxMld3SFFyMUlJM2VEZzN3cGk0NnlWQ1ZaR2ZXVTc1Z1JlbzBUVDR3dE5iaWlOZWwvdHkybVFrdQ",
            "external_order_id": "2023051611420539815"
        }
        headers = {
            "accept": "application/json",
            "Authorization": "sha512-mQjovu3w7j+Ub1L/P3BH6a9PPPGOgEPjzqsqcsGXJqfY7slwuwTIcXFQIyXYiN7SdGSiIQHrvaO9yo4WAtYktA==?4ca7",
            "content-type": "application/json"
        }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)