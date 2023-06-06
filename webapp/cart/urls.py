from django.urls import path, include

from cart.views.cartDetailAPIView import CartDetailAPIView
from cart.views.cartListAPIView import CartListAPIView
from cart.views.croneSendGiftAPIView import CroneSendGiftAPIView

app_name = 'cart'

urlpatterns = [
    path('', CartListAPIView.as_view()),
    path('<uuid:uuid>/', CartDetailAPIView.as_view()),
    path('payments/', include('payment.urls'), name='kakaopay'),
    path('<uuid:uuid>/sendgift/',CroneSendGiftAPIView.as_view())
]
