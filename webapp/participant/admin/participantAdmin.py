from django.contrib import admin

from participant.models import Participant
from survey.models import Survey


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj is None:  # post
            form.base_fields['user'].initial = request.user
            form.base_fields['user'].disabled = True

            form.base_fields['survey'].queryset = Survey.objects.exclude(writer=request.user)
        else:  # update
            if obj.user == request.user:
                form.base_fields['user'].disabled = True
                form.base_fields['survey'].queryset = Survey.objects.exclude(writer=request.user)
            else:
                form.base_fields['user'].disabled = True
                form.base_fields['survey'].disabled = True
                form.base_fields['json'].disabled = True

        return form

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.user == request.user:
            return True
        else:
            return False
