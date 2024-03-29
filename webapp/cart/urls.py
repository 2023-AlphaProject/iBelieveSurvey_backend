from django.urls import path, include

from cart.views import CartDetailAPIView
from cart.views import CartListAPIView

app_name = 'cart'

urlpatterns = [
    path('', CartListAPIView.as_view()),
    path('<uuid:uuid>/', CartDetailAPIView.as_view()),
    path('payments/', include('payment.urls'), name='kakaopay'),
]
