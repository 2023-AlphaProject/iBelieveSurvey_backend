from django.urls import path

from cart.views.cartDetailAPIView import CartDetailAPIView
from cart.views.cartListAPIView import CartListAPIView

urlpatterns = [
    path('', CartListAPIView.as_view()),
    path('<int:pk>/', CartDetailAPIView.as_view()),
]
