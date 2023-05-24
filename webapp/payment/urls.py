from django.urls import path
from payment.views import KakaoPayAPI

urlpatterns = [
    path('', KakaoPayAPI.as_view()),
]
