from django.contrib import admin

from gifticon.models import SurveyGifticon


@admin.register(SurveyGifticon)
class SurveyGifticonAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'gifticon', 'count', 'receiver')



