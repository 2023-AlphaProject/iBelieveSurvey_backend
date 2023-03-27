from django.contrib import admin

from participant.models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'kakaoId', 'survey', 'json',)
