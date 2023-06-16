import profile
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
from django.contrib.auth import authenticate, login
from user.serializers import UserViewSerializer

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

    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me',
                                      headers={"Authorization": f'Bearer ${access_token}'})

    profile_json = user_info_response.json()
    print("profile_json!!!!!!!!", profile_json)

    kakao_account = profile_json.get("kakao_account")
    kakaoId = profile_json.get("id")
    print("kakao_account!!!!!!!!!!!!!!!!!!!!", kakao_account)
    print("profile_json!!!!!!!!", profile_json)
    email = kakao_account.get("email", None)

    if email is None:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     user_info = User.objects.get(kakaoId=kakaoId)
    #     encoded_jwt = jwt.encode({'id': user_info.kakaoId}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행 
    #     response = HttpResponse()
    #     response.set_cookie('jwt_token', encoded_jwt) 
    #     return response

    # except User.DoesNotExist:
    #     data = {
    #           'kakaoId': kakaoId,
    #           'email' : email,
    #           'password': '1234',
    #           # 비밀번호는 없지만 validation 을 통과하기 위해서 임시로 사용
    #           # 비밀번호를 입력해서 로그인하는 부분은 없으므로 안전함
    #         }
            
    #     serializer = UserViewSerializer(data=data)
    #     if not serializer.is_valid():
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     user = serializer.validated_data
    #     serializer.create(validated_data=user)

    #         # 2-1. 회원가입 하고 토큰 만들어서 쿠키에 저장하기
    #     try:
    #         user_info = User.objects.get(kakaoId=kakaoId)
    #         encoded_jwt = jwt.encode({'id': user_info.kakaoId}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행 
    #         response = HttpResponse()
    #         response.set_cookie('jwt_token', encoded_jwt) 
    #         return response
    #     except:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)





    # 카카오톡 계정이 DB에 저장되어 있는지 확인
    if User.objects.filter(kakaoId=kakaoId).exists():
        user_info = User.objects.get(kakaoId=kakaoId)

        # jwt 방식
        encoded_jwt = jwt.encode({'id': user_info.kakaoId}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행 
        # # return HttpResponse(f'id:{user_info.kakaoId}, token:{encoded_jwt}, exist:true')
        # # user = User.objects.get(kakaoId=kakaoId)
        # user = authenticate(request, user=user_info)  # 사용자 인증
        # # if user is not None:
        # login(request, user)  # 인증된 사용자로 로그인
        # print("2222222222")
        #     # return super().create(request, *args, **kwargs)

        # return JsonResponse({'access_token': encoded_jwt}, status=201)
        return HttpResponse(f'id:{user_info.kakaoId}, token:{encoded_jwt}, email:{email}, exist:true')

    # 저장되어 있지 않다면 회원가입 
    else:
        User(
            kakaoId=kakaoId,
            email=email,
        ).save()
        user_info = User.objects.get(kakaoId=kakaoId)
        serializer = UserViewSerializer(data=user_info)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # jwt 방식
        encoded_jwt = jwt.encode({'id': user_info.kakaoId}, SECRET_KEY, algorithm='HS256')
        # return HttpResponse(f'id:{user_info.kakaoId}, token:{encoded_jwt}, exist:true')
        # user = authenticate(request, user=user_info)  # 사용자 인증
        # # if user is not None:
        #     login(request, user)  # 인증된 사용자로 로그인
        #     print("111111111")
            # return super().create(request, *args, **kwargs)
        return HttpResponse(f'id:{user_info.kakaoId}, token:{encoded_jwt}, email:{email}, exist:true')
        # return JsonResponse({'access_token': encoded_jwt}, status=201)
