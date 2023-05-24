from django.urls import path, include

from cart.views.cartDetailAPIView import CartDetailAPIView
from cart.views.cartListAPIView import CartListAPIView

app_name = 'cart'

urlpatterns = [
    path('', CartListAPIView.as_view()),
    path('<int:cart_id>/', CartDetailAPIView.as_view()),
    path('payments/', include('payment.urls'), name='kakaopay'),
]
