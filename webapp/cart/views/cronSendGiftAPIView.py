import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from order.models import Order
from template.models import Template
from user.models import User
from config.settings.base import SOCIAL_OUTH_CONFIG
import os

class CronSendGiftAPIView(APIView):
     def post(self, request, survey_id, uuid):

        success_callback_url = "https://ibelievesurvey.com/" # 일단 localhost로 고정 -> 나중에 수정 필요
        fail_callback_url = "https://ibelievesurvey.com/" # 일단 localhost로 고정 -> 나중에 수정 필요
        receiver_type = "PHONE"
        CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
        template_token_list_str = os.environ.get("TEMPLATE_TOKEN_LIST") 
        template_token_list = eval(template_token_list_str)
        print("토큰리스트~", template_token_list)

        try:
            # cart = Cart.objects.filter(is_sent=False)
            order_list = Order.objects.filter(cart = uuid)
            if len(order_list) == 0:
                return Response({"error": "잘못된 장바구니 접근 입니다."}, status=400)
            print(order_list)

            for order in order_list:
                receiver = order.receiver
                cart = order.cart

                kakaoId = receiver.user.kakaoId
                template_id = cart.template_id
                user = User.objects.get(kakaoId=kakaoId)
                template = order.cart.template 

                phone_number = user.phoneNumber
                if len(phone_number)==13 and phone_number[3]=="-" and phone_number[8]=="-": # 010-1234-5678 -> 13자
                    phone_number = user.phoneNumber
                else:
                    formatted_number = phone_number[:3] + '-' + phone_number[3:7] + '-' + phone_number[7:]
                    phone_number = formatted_number

                real_name = user.realName
                template_order_name = template.template_name
                print("템플릿 이름", template_order_name)
                print(real_name)
                print(phone_number)

                for item in template_token_list:
                    if str(template_order_name) in item:
                        template_token = item[template_order_name]
                        print("템플릿 토큰~",template_token)
                        break

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
                    "external_order_id": str(uuid) + str(order.id) 
                }

                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "Authorization": "KakaoAK " + CLIENT_ID
                }

                # 선물 발송 API 요청 보내기
                response = requests.post("https://gateway-giftbiz.kakao.com/openapi/giftbiz/v1/template/order", json=payload, headers=headers)

                if response.status_code != status.HTTP_200_OK:
                    print("Request Payload:", payload)
                    print("headers:", headers)
                    print("Response Content:", response.content)
                    return Response({"message": "선물 발송 요청 실패. " + response.text}, status=response.status_code)
                    # return Response({"message": "선물 발송 요청 실패."}, status=response.status_code)

            return Response({"message": "선물 발송 요청 성공."}, status=status.HTTP_200_OK)

        except (Order.DoesNotExist, User.DoesNotExist):
            return Response({"message": "Required data not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
