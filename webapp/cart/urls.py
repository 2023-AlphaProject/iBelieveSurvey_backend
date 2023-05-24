from django.urls import path, include

from cart.views.cartDetailAPIView import CartDetailAPIView
from cart.views.cartListAPIView import CartListAPIView

urlpatterns = [
    path('carts/', CartListAPIView.as_view()),
    path('carts/<int:survey_id>/', CartDetailAPIView.as_view()),
    path('payments/', include('payment.urls'), name='kakaopay'),
]
