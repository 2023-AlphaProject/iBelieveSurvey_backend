from rest_framework import serializers

from template.models import Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            'pk', 'template_name', 'template_trace_id', 'order_template_status', 'budget_type',
            'gift_sent_count', 'bm_sender_name', 'mc_image_url', 'mc_text', 'item_type', 'product_name',
            'brand_name', 'product_image_url', 'product_thumb_image_url', 'brand_image_url', 'product_price'
        ]
        read_only_fields = [
            'pk', 'template_name', 'template_trace_id', 'order_template_status', 'budget_type',
            'gift_sent_count', 'bm_sender_name', 'mc_image_url', 'mc_text', 'item_type', 'product_name',
            'brand_name', 'product_image_url', 'product_thumb_image_url', 'brand_image_url', 'product_price'
        ]
        # template_token을 제외한 모든 필드
