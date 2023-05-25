from django.urls import path
from payment.views import KakaoPayAPI, KakaoPaySuccess

urlpatterns = [
    path('', KakaoPayAPI.as_view()),
    path('success', KakaoPaySuccess.as_view()),
]
