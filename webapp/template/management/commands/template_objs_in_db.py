import ast
import os
import requests
from django.core.management.base import BaseCommand

from template.models import Template


class Command(BaseCommand):
    def handle(self, *args, **options):
        template_token_dict_list_str = os.environ.get("TEMPLATE_TOKEN_LIST")
        template_token_dict_list = ast.literal_eval(template_token_dict_list_str)
        template_token_num = len(template_token_dict_list)

        product_url_dict_list = [
            {'공차 밀크티': '6881256'},
            {'할리스 에스프레소': '4653370'},
            {'투썸플레이스 아메리카노': '4072511'},
        ]

        url = "https://gateway-giftbiz.kakao.com/openapi/giftbiz/v1/template"
        api_key = "KakaoAK " + os.environ.get("KAKAO_GIFT_BIZ_REST_APP_KEY")
        headers = {
            "Authorization": api_key,
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        json_data = response.json()
        templates = json_data["contents"]  # [{"":""}, {"":""}, {"": {"":""}, {"":""}}] 형태

        if Template.objects.exists():
            if Template.objects.count() == template_token_num:
                print("")
                print("######################################################")
                print("############ 빌드가 실행된 적이 있습니다. ############")
                print("## DB 템플릿 객체 개수 == .env 파일의 환경변수 개수 ##")
                print("###### 템플릿 객체 업데이트를 진행하지 않습니다. #####")
                print("######################################################")
                print("")

                template_objs = Template.objects.all()
                for template_obj in template_objs:
                    print(template_obj.template_token)
                return

            else:
                print("")
                print("######################################################")
                print("############ 빌드가 실행된 적이 있습니다. ############")
                print("## DB 템플릿 객체 개수 != .env 파일의 환경변수 개수 ##")
                print("######### 템플릿 객체 업데이트를 진행합니다. #########")
                print("######################################################")
                print("")

                Template.objects.all().delete()
        else:
            print("")
            print("######################################################")
            print("############ 빌드가 실행된 적이 없습니다. ############")
            print("########### 템플릿 객체 생성을 진행합니다. ###########")
            print("######################################################")
            print("")

        for template_token_dict, product_url_dict in zip(template_token_dict_list, product_url_dict_list):

            for template in templates:
                template_name = template["template_name"]

                if template_name in template_token_dict and template_name in product_url_dict:
                    template_token = template_token_dict[template_name]
                    product_detail_url = "https://gift.kakao.com/product/" + product_url_dict[template_name]

                    # 템플릿 정보에서 필요한 데이터 추출
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

                    # 템플릿 객체 생성 및 저장
                    new_template = Template(
                        product_detail_url=product_detail_url,
                        template_token=template_token,
                        template_name=template_name,

                        template_trace_id=template_trace_id,
                        order_template_status=order_template_status,
                        budget_type=budget_type,
                        gift_sent_count=gift_sent_count,
                        bm_sender_name=bm_sender_name,
                        mc_image_url=mc_image_url,
                        mc_text=mc_text,

                        item_type=item_type,
                        product_name=product_name,
                        brand_name=brand_name,
                        product_image_url=product_image_url,
                        product_thumb_image_url=product_thumb_image_url,
                        brand_image_url=brand_image_url,
                        product_price=product_price
                    )
                    new_template.save()
        print("")
        print("######################################################")
        print("### 템플릿 객체 생성 및 업데이트가 완료되었습니다. ###")
        print("######################################################")
        print("")
