import requests
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config.settings.base import SOCIAL_OUTH_CONFIG
from django.http import JsonResponse
from rest_framework import status
from user.models import User
from config.settings.base import SECRET_KEY
from django.http import HttpResponse
import jwt

@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoGetLogin(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRET_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRET_URL}&response_type=code"
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
        "client_id": SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
        "redirect_uri": SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
        'code': code,
    }
    token_response = requests.post(url, data=res)
    print(token_response.json())
    access_token = token_response.json().get('access_token')

    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})

    profile_json = user_info_response.json()

    kakao_account = profile_json.get("kakao_account")
    kakaoId = profile_json.get("id")
    email = kakao_account.get("email", None) 

    if email is None:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    # 카카오톡 계정이 DB에 저장되어 있는지 확인
    if User.objects.filter(kakaoId=kakaoId).exists():  
        user_info = User.objects.get(kakaoId=kakaoId)  
        encoded_jwt = jwt.encode({'id': user_info.kakaoId}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행
        return HttpResponse(f'id:{user_info.kakaoId}, token:{encoded_jwt}, exist:true')

    # 저장되어 있지 않다면 회원가
    else:
        User(
            kakaoId = kakaoId,
            email = email, 
        ).save()
        user_info = User.objects.get(kakaoId=kakaoId)
        encoded_jwt = jwt.encode({'id': user_info.kakaoId}, SECRET_KEY, algorithm='HS256')  
        return HttpResponse(f'id:{user_info.kakaoId}, token:{encoded_jwt}, exist:true')
    
# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def logout(self,request):
#         res = Response()
#         res.delete_cookie('encoded_jwt')
#         res.data = {
#             "message" : 'success'
#         }
#         return res
