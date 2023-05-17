# from django.urls import path

# from user.views import KakaoLoginView

# # from user.views import views

# urlpatterns = [
#     path('kakao/callback/', KakaoLoginView.as_view()),
#     # path('kakao/',views.kakaoGetLogin,name="kakaoGetLogin"),
#     # path('kakao/callback', views.kakaoCallback,name="kakaoCallback"),
# ]


from django.urls import path

from user.views.kakaoUserView import kakaoCallback
from user.views.kakaoUserView import kakaoGetLogin

urlpatterns = [
    path('kakao/login',kakaoGetLogin),
    path('kakao/callback', kakaoCallback, name="kakaoCallback")
]
