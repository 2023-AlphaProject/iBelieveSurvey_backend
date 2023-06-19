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
            {"퍼페티)츄파춥스":"7209457"},
            {"디카페인 카페 아메리카노 T":"4165669"},
            {"카라멜 마키아또 T":"4165635"},
            {"카페 라떼 T 2잔+슈크림 가득 바움쿠헨": "3818518"},
            {"카페 아메리카노 T 2잔+블루베리 쿠키 치즈 케이크": "3818639"},
            {"카페 아메리카노 T 2잔+클라우드 치즈 케이크": "3818616"},
            {"카페 아메리카노 T+7 레이어 가나슈 케이크": "3818648"},
            {"제주 유기농 말차로 만든 크림 프라푸치노 T": "4166033"},
            {"쿨 라임 피지오 T": "4165855"},
            {"자몽 허니 블랙 티 T": "4165956"},
            {"카페 라떼 T": "3818402"},
            {"아이스 카페 아메리카노 T": "3818654"},
            {"돌체 콜드 브루 T": "4165666"},
            {"딸기 딜라이트 요거트 블렌디드": "4165696"},
            {"자바 칩 프라푸치노 T": "4165964"}
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
