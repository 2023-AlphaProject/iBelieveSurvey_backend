from django.urls import path

from user.views.kakaoUserView import kakaoCallback
from user.views.kakaoUserView import kakaoGetLogin
from user.views.myPagePaidAPIView import MyPagePaidAPIView
from user.views.userAPIView import UpdateUserAPIView
from user.views.myPageParticipatedAPIView import MyPageParticipatedAPIView

urlpatterns = [
    path('kakao/login', kakaoGetLogin),
    path('kakao/callback', kakaoCallback, name="kakaoCallback"),
    path('update', UpdateUserAPIView.as_view()),
    path('mypage/paid/', MyPagePaidAPIView.as_view()),
    path('mypage/participated/', MyPageParticipatedAPIView.as_view()),
]
