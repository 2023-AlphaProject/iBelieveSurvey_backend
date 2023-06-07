import os
import re
from datetime import datetime

import requests
from rest_framework import status

from config.settings.base import SOCIAL_OUTH_CONFIG
from order.models import Order
from participant.models import Participant


def assignReciver():
    orders = Order.objects.filter(receiver=None)

    if orders.count() == 0:
        print("이미 모든 설문에 당첨자가 지정되어 있습니다." + str(datetime.now()))
        return
    print("랜덤 당첨자 선정 시작 : " + str(datetime.now()))
    print("--------------------------------------------")
    exclude_receivers = []

    for order in orders:

        cart = order.cart
        survey = cart.survey

        if survey.is_end:
            available_receivers = Participant.objects.filter(survey=order.cart.survey).exclude(
                user__in=exclude_receivers)
            print(available_receivers)
            if available_receivers.exists():
                random_receiver = available_receivers.order_by('?').first()
                exclude_receivers.append(random_receiver.user)
                order.receiver = random_receiver
                receiver = random_receiver.user
                template = order.cart.template
                if not sendGifticon(receiver, template):
                    order.receiver = None
                order.save()
                print("설문 : " + order.cart.survey.title)
                print("당첨자 : " + random_receiver.user.realName)
                print("기프티콘 : " + order.cart.template.template_name)
                print("--------------------------------------------")

        else:
            print("설문 : " + order.cart.survey.title)
            print("해당 설문은 종료되지 않았기 때문에 당첨자를 지정하지 않고 다음 설문으로 넘어가 작업을 수행합니다.")
    print("랜덤 당첨자 선정 종료")
    print("--------------------------------------------")
    return


def sendGifticon(receiver, template):
    success_callback_url = "https://ibelievesurvey.com/"  # 일단 localhost로 고정 -> 나중에 수정 필요
    fail_callback_url = "https://ibelievesurvey.com/"  # 일단 localhost로 고정 -> 나중에 수정 필요
    receiver_type = "PHONE"
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    template_token_list_str = os.environ.get("TEMPLATE_TOKEN_LIST")
    template_token_list = eval(template_token_list_str)
    print("--------------------------------------------")
    print("선물 발송 시작 : " + str(datetime.now()))

    user = receiver
    phone_number = receiver.phoneNumber
    phone_number_pattern = r'^010-\d{4}-\d{4}$'

    if not re.match(phone_number_pattern, phone_number):
        print("----------------------")
        print("기프티콘 발송 실패 : 전화번호 형식이 맞지 않습니다.")
        print("----------------------")
        return False

    real_name = user.realName
    template_order_name = template.template_name
    print("기프티콘 종류 : ", template_order_name)
    print("받는 사람 : ", real_name)
    print("휴대폰 번호 : ", phone_number)

    template_token = ""
    for item in template_token_list:
        if str(template_order_name) in item:
            template_token = item[template_order_name]
            break

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
        "external_order_id": user.id,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "KakaoAK " + CLIENT_ID
    }

    # 선물 발송 API 요청 보내기
    response = requests.post("https://gateway-giftbiz.kakao.com/openapi/giftbiz/v1/template/order",
                             json=payload, headers=headers)

    if response.status_code != status.HTTP_200_OK:
        print("----------------------")
        print("기프티콘 발송 실패")
        print("----------------------")
        print("Request Payload:", payload)
        print("headers:", headers)
        print("Response Content:", response.content)
        return False
    else:
        print("----------------------")
        print("기프티콘 발송 성공")
        print("----------------------")
        return True
