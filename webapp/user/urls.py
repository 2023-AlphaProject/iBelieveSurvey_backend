from django.urls import path

from user.views import kakaoCallback

urlpatterns = [
    path('kakao/callback', kakaoCallback)
]
