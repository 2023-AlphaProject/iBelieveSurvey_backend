from rest_framework.generics import RetrieveAPIView

from order.models import Order
from order.serializers import OrderSerializer


class OrderDetailAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
