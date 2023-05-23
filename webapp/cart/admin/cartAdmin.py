from django.contrib import admin

from cart.models import Cart
from survey.models import Survey


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):  # admin 페이지에서 form을 가져올 때 호출됨. (즉 POST할 때)
        form = super().get_form(request, obj, **kwargs)

        if obj is None:  # post
            form.base_fields['survey'].queryset = Survey.objects.filter(user=request.user)
        else:  # update
            if obj.survey.user == request.user and obj.survey.is_idle:
                form.base_fields['survey'].queryset = Survey.objects.filter(user=request.user)
            else:
                form.base_fields['survey'].disabled = True
                form.base_fields['template'].disabled = True
                form.base_fields['quantity'].disabled = True

        return form

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.survey.user == request.user:
            return True
        else:
            return False


# survery객체 생성되는 시점 (survey객체 임시저장)
# is_idle=True, is_awarded=False, is_ongoing=False, is_done=False.

# survey객체가 gifticon객체와 연결된 시점 (survey객체 생성완료)
# is_idle=False, is_awarded=False, is_ongoing=True, is_done=False.

# survey객체의 end_at 필드가 시간 초과된 시점(surveey객체 종료)
# is_idle=False, is_awarded=False, is_ongoing=False, is_done=True.

# gifticon객체가 전송된 시점()
# is_idle=False, is_awarded=True, is_ongoing=False, is_done=False.
