from rest_framework import serializers

from cart.models import Cart
from template.serializers import TemplateSerializer


class CartListSerializer(serializers.ModelSerializer):
    template = TemplateSerializer()

    total_price = serializers.SerializerMethodField()
    result_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "uuid",
            "survey",
            "template",
            "quantity",
            "total_price",
            'result_price',
            "is_sent"
        ]
        read_only_fields = [
            "uuid",
            "survey",
            "total_price",
            'result_price'
        ]
        depth = 1

    def get_total_price(self, obj):
        return obj.total_price

    def get_result_price(self, objs):
        queryset = self.context['view'].get_queryset()
        result_price = sum(cart.total_price for cart in queryset)
        return result_price
