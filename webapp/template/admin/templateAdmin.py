from django.contrib import admin

from template.models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'template_token', 'template_name', 'template_trace_id', 'start_at', 'end_at',
                    'order_template_status', 'budget_type', 'gift_budget_count', 'gift_sent_count', 'gift_stock_count',
                    'bm_sender_name', 'mc_image_url', 'mc_text', 'product')
