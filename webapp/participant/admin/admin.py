from django.contrib import admin

from participant.models import Participant

@admin.register(Participant)
class GifticonAdmin(admin.ModelAdmin):
    list_display = ('id', 'kakaoId', 'survey', 'json',)
