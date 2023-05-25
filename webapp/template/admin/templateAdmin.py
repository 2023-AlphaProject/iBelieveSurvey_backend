from django.contrib import admin

from template.models.template import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'template_name', 'template_trace_id', 'order_template_status',
        'budget_type', 'gift_sent_count', 'bm_sender_name', 'mc_image_url', 'mc_text',

        'item_type', 'product_name', 'brand_name', 'product_image_url',
        'product_thumb_image_url', 'brand_image_url', 'product_price'
    )
