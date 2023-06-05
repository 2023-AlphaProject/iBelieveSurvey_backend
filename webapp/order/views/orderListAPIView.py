from rest_framework.generics import ListAPIView

from order.models import Order
from order.serializers import OrderSerializer


class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
