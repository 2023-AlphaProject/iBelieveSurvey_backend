from django.urls import path

from user.views.kakaoUserView import kakaoCallback

urlpatterns = [
    path('user/kakao/callback', kakaoCallback )
]