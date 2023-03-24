from django.shortcuts import redirect
from webapp.config.settings.base import SOCIAL_OUTH_CONFIG
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoGetLogin(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRET_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        CLIENT_ID, REDIRET_URL)
    return redirect(url)