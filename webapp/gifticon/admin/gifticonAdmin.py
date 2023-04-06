from django.contrib import admin

from gifticon.models import Gifticon


@admin.register(Gifticon)
class GifticonAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'productImage', 'productName', 'gifticonType', )
