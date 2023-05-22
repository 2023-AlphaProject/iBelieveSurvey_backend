from django.urls import path

from user.views.kakaoUserView import kakaoCallback
from user.views.kakaoUserView import kakaoGetLogin
from user.views.userAPIView import UpdateUserAPIView

urlpatterns = [
    path('kakao/login',kakaoGetLogin),
    path('kakao/callback', kakaoCallback, name="kakaoCallback"),
    path('update', UpdateUserAPIView.as_view()),
]
