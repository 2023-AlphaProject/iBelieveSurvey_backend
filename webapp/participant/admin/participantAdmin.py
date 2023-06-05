from django.contrib import admin

from participant.models import Participant
from survey.models import Survey


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'survey', 'created_at')
    ordering = ('id',)

    def name(self, obj):
        return obj.user.realName

    def survey(self, obj):
        return obj.survey.title
