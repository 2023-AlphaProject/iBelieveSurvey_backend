import requests
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from config.settings.base import SOCIAL_OUTH_CONFIG

@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoGetLogin(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRET_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(CLIENT_ID, REDIRET_URL)
    return redirect(url)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoCallback(request):
    url = "https://kauth.kakao.com/oauth/token"
    code = request.GET.get("code")
    if code is None:
        raise Exception("code is none")

    res = {
        'grant_type': 'authorization_code',
        'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
        'code': code
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)

    tokenJson = response.json()
    userUrl = "https://kapi.kakao.com/v2/user/me"  # 유저 정보 조회하는 uri
    auth = "Bearer " + tokenJson['access_token']  ## 'Bearer '여기에서 띄어쓰기 필수!!
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(userUrl, headers=HEADER)
    return Response(res.text)



# import requests
# from django.shortcuts import redirect
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from django.http import JsonResponse
# from config.settings.base import SOCIAL_OUTH_CONFIG

# class KakaoLoginView():

#     def kakaoGetLogin(request):
#         CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
#         REDIRET_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
#         if CLIENT_ID is None:
#             raise Exception("CLIENT_ID is none")
#         url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRET_URL}&response_type=code"
#         if url =="https://kauth.kakao.com/oauth/authorize?client_id=c177823802a7ea7d3b1cf9ff257b0785&redirect_uri=http://localhost/user/kakao/callback&response_type=code":
#             raise Exception("same")
#         return redirect(url)


#     def kakaoCallback(request):
#         auth_code = request.GET.get('code')
#         if auth_code is None:
#             raise Exception("code is none")
#         kakao_token_api = 'https://kauth.kakao.com/oauth/token'
#         data = {
#                 'grant_type': 'authorization_code',
#                 'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
#                 'redirection_uri': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
#                 'code': auth_code
#             }
#         token_response = requests.post(kakao_token_api, data=data)
#         access_token = token_response.json().get('access_token')

#         return access_token
#     # user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
#     # return JsonResponse({"user_info": user_info_response.json()})



#     # url = "https://kauth.kakao.com/oauth/token"
#     # code = request.GET.get("code")
#     # if code is None:
#     #     raise Exception("code is none")

#     # res = {
#     #     'grant_type': 'authorization_code',
#     #     'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
#     #     'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
#     #     'client_secret': "",
#     #     'code': code
#     # }
#     # headers = {
#     #     'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
#     # }
#     # response = requests.post(url, data=res, headers=headers)

#     # tokenJson = response.json()
#     # userUrl = "https://kapi.kakao.com/v2/user/me"  # 유저 정보 조회하는 uri
#     # auth = "Bearer " + tokenJson['access_token']  ## 'Bearer '여기에서 띄어쓰기 필수!!
#     # HEADER = {
#     #     "Authorization": auth,
#     #     "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
#     # }
#     # res = requests.get(userUrl, headers=HEADER)
#     # return Response(res.text)

    

