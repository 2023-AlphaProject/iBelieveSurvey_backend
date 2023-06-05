from django.urls import path

from order.views import OrderDetailAPIView
from order.views import OrderListAPIView

app_name = 'order'

urlpatterns = [
    path('<int:pk>/', OrderDetailAPIView.as_view()),
    path('', OrderListAPIView.as_view()),
]
