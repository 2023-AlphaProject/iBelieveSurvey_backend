from django.contrib import admin

from survey.models import Survey


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'status', 'end_at', 'created_at')
    list_filter = ('category', 'status', 'created_at')
