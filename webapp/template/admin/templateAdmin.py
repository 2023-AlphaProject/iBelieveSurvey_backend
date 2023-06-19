from django.contrib import admin

from template.models.template import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'template_name',
        'gift_sent_count',
        'product_name',
        'brand_name',
        'product_price'
    )
