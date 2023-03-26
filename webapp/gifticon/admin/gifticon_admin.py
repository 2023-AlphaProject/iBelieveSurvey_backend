from django.contrib import admin

from gifticon.models import Gifticon


@admin.register(Gifticon)
class GifticonAdmin(admin.ModelAdmin):
    list_display = ('survey_id', 'if_sent', 'count', 'gifticon_type', 'sender', 'receiver')
    list_filter = ('if_sent', 'gifticon_type', 'created_at')



