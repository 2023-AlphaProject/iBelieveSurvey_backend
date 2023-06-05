from rest_framework.generics import RetrieveAPIView, APIView
import requests
from rest_framework import status
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer
from order.models import Order
from template.models import Template
from cart.models import Cart
from user.models import User
from participant.models import Participant


class OrderDetailAPIView(RetrieveAPIView,APIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def post(self, request, order_id):

        success_callback_url = "localhost:3000" # 일단 localhost로 고정 -> 나중에 수정 필요
        fail_callback_url = "localhost:3000" # 일단 localhost로 고정 -> 나중에 수정 필요
        receiver_type = "PHONE"

        try:
            # Order 모델에서 cart와 receiver 정보 가져오기
            order = Order.objects.get(id=order_id)
            # order = Order.objects.select_related('cart', 'receiver').get(pk=request.data['order_id'])

            for _ in range(order.cart.quantity):
                receiver = order.receiver
                cart = order.cart

                kakaoId = receiver.kakaoId
                template_id = cart.template_id
                user = User.objects.select_related('participant').get(kakaoId=kakaoId)
                template = Template.objects.select_related('cart').get(template_id=template_id)

                phone_number = user.phoneNumber
                if len(phone_number)==13 and phone_number[3]=="-" and phone_number[8]=="-": # 010-1234-5678 -> 13자
                    phone_number = user.phoneNumber
                else:
                    formatted_number = phone_number[:3] + '-' + phone_number[3:7] + '-' + phone_number[7:]
                    phone_number - formatted_number
                    
                real_name = user.realName
                template_token = template.template_token
                template_order_name = template.template_name
                template_trace_id = template.template_trace_id

                payload = {
                    "template_token": template_token,
                    "receiver_type": receiver_type,
                    "receivers": [{
                        "name": real_name,
                        "receiver_id": phone_number
                    }],
                    "success_callback_url": success_callback_url,
                    "fail_callback_url": fail_callback_url,
                    "template_order_name": template_order_name,
                    "external_order_id": str(cart.uuid) + str(order_id) # 임의로 넣어놓음. 
                }

                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "Authorization": "KakaoAKf49e58b9e6f3d2cc175679f1c5534ca7"
                }

                # 선물 발송 API 요청 보내기
                response = requests.post("https://gateway-giftbiz.kakao.com/openapi/giftbiz/v1/template/order", json=payload, headers=headers)

                if response.status_code != status.HTTP_200_OK:
                    return Response({"message": "선물 발송 요청 실패."}, status=response.status_code)

            return Response({"message": "선물 발송 요청 성공."}, status=status.HTTP_200_OK)

        except (Order.DoesNotExist, User.DoesNotExist):
            return Response({"message": "Required data not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
