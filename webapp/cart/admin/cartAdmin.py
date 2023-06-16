from django.contrib import admin

from cart.models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'survey', 'template', 'quantity', 'is_sent')