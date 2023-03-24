from django.urls import path

from webapp.user.views.kakaoUserView import kakaoCallback

urlpatterns = [
    path('user/kakao/callback', kakaoCallback )
]