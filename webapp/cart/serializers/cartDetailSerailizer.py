from rest_framework import serializers

from cart.models import Cart
from template.models import Template


class CartDetailSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all())

    class Meta:
        model = Cart
        fields = [
            "uuid",
            "survey",
            "template",
            "quantity",
        ]
        read_only_fields = [
            "uuid",
            "survey",
        ]
        depth = 1
