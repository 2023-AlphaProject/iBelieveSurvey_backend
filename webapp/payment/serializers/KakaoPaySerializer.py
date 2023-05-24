from rest_framework import serializers


class KakaoPaySerializer(serializers.Serializer):
    cid = serializers.CharField(
        max_length=255,
    )
    partner_order_id = serializers.CharField(
        max_length=255
    )
    partner_user_id = serializers.CharField(
        max_length=255
    )
    item_name = serializers.CharField(
        max_length=255
    )
    quantity = serializers.IntegerField()
    total_amount = serializers.IntegerField()
    tax_free_amount = serializers.IntegerField()
    approval_url = serializers.URLField(
        max_length=255
    )
    cancel_url = serializers.URLField(
        max_length=255
    )
    fail_url = serializers.URLField(
        max_length=255
    )
