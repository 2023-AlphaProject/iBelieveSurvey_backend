from rest_framework import serializers

from template.models import Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            'id', 'product_detail_url', 'template_name', 'bm_sender_name', 'mc_image_url',
            'product_name', 'brand_name', 'product_image_url', 'product_thumb_image_url',
            'brand_image_url', 'product_price'
        ]
        read_only_fields = [
            'id', 'product_detail_url', 'template_name', 'bm_sender_name', 'mc_image_url',
            'product_name', 'brand_name', 'product_image_url', 'product_thumb_image_url',
            'brand_image_url', 'product_price'
        ]
        # template_token을 제외한 모든 필드
        depth = 2
