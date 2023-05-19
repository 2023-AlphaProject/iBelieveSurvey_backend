import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import requests
from django.core.management.base import BaseCommand
from template.models import Template

script_absol_dir = os.path.dirname(os.path.abspath(__file__))
env_absol_dir = os.path.join(script_absol_dir, '../../../.env')

template_token_list = []


class Command(BaseCommand):
    help = 'Create template objects and save in DB'

    def handle(self, *args, **options):
        # .env 파일 읽기
        with open(env_absol_dir, "r", encoding="utf-8") as file:

            app_key_dict = {}

            for line in file:
                # 주석 또는 빈 줄은 건너뜀
                if line.startswith("#") or line.strip() == "":
                    continue

                elif line.startswith("KAKAO_GIFT_BIZ_REST_APP_KEY"):
                    key, value = line.strip().split("=")
                    value = value.strip("\'")
                    app_key_dict[key] = value

                elif line.startswith("TEMPLATE_TOKEN_LIST"):
                    # TEMPLATE_TOKEN_LIST=\r\n
                    # [\r\n
                    # {'공차 밀크티':'b3dPNnRSZ2QwSzFvdERFdjhJQkZEanI1dmFvcXoxeVY5UzIvL3BleWovaGZGNk9Ta1NuZEk5Qk1uN0NxWWFOQg'},\r\n
                    # {'할리스 에스프레소':'XVnY3JiT3dObXR3NHNrWWNMNG13WUtJWkZwbmhJOU9aVXJMM0ViWTF3U0haSU1QbmRmcUVyaw'},\r\n
                    # {'투썸플레이스 아메리카노':'bjZ1d1QvaGNoWDJJY3RCYXNOZnB6YzRKMG8xNktKRXR5aEJ1a0Zpa2RVVVBSdWh0QWVRRVI2dU9N},\r\n
                    # ]
                    while True:  # TEMPLATE_TOKEN_LIST의 시작 라인을 찾았을 때 로직 구현
                        line = file.readline().strip()

                        if line.startswith("["):
                            continue

                        elif not line or line.endswith("]"):
                            break

                        else:
                            template_token_dict = {}

                            now_use_dict = line.strip("\r\n").strip(",")
                            key, value = now_use_dict.strip("{").strip("}").split(":")
                            key = key.strip("\'")
                            value = value.strip("\'")
                            # print(f"key:{key}, value:{value}")

                            template_token_dict[key] = value
                            template_token_list.append(template_token_dict)

        url = "https://gateway-giftbiz.kakao.com/openapi/giftbiz/v1/template"
        api_key = "KakaoAK " + app_key_dict["KAKAO_GIFT_BIZ_REST_APP_KEY"]
        headers = {
            "Authorization": api_key,
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        json_data = response.json()  # response객체로부터 JSON 추출
        total_count = json_data["totalCount"]
        templates = json_data["contents"]

        # 템플릿이 중복되어 저장되지 않도록 DB에 저장되어 있던 기존 템플릿들을 삭제한다.
        Template.objects.all().delete()

        # 응답에 실려온 template_name 추출해서 리스트에 담는다.
        for n in range(0, total_count):
            template = templates[n]
            template_name = template["template_name"]

            for template_token_list_dict in template_token_list:

                if template_name in template_token_list_dict:
                    template_token = template_token_list_dict[template_name]

                    # template_name 변수는 이미 위에서 생성
                    template_trace_id = template["template_trace_id"]
                    order_template_status = template["order_template_status"]
                    budget_type = template["budget_type"]
                    gift_sent_count = template["gift_sent_count"]
                    bm_sender_name = template["bm_sender_name"]
                    mc_image_url = template["mc_image_url"]
                    mc_text = template["mc_text"]

                    product_data = template["product"]

                    item_type = product_data["item_type"]
                    product_name = product_data["product_name"]
                    brand_name = product_data["brand_name"]
                    product_image_url = product_data["product_image_url"]
                    product_thumb_image_url = product_data["product_thumb_image_url"]
                    brand_image_url = product_data["brand_image_url"]
                    product_price = product_data["product_price"]

                    new_template = Template(template_token=template_token, template_name=template_name,
                                            template_trace_id=template_trace_id,
                                            order_template_status=order_template_status,
                                            budget_type=budget_type, gift_sent_count=gift_sent_count,
                                            bm_sender_name=bm_sender_name, mc_image_url=mc_image_url,
                                            mc_text=mc_text, item_type=item_type,
                                            product_name=product_name, brand_name=brand_name,
                                            product_image_url=product_image_url,
                                            product_thumb_image_url=product_thumb_image_url,
                                            brand_image_url=brand_image_url, product_price=product_price)

                    new_template.save()
        print("save!")
