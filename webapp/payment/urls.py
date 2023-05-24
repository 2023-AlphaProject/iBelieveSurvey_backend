from django.urls import path

from cart.views.cartDetailAPIView import CartDetailAPIView
from cart.views.cartListAPIView import CartListAPIView

urlpatterns = [
    path('carts/', CartListAPIView.as_view()),
    path('carts/<int:survey_id>/', CartDetailAPIView.as_view()),
]
