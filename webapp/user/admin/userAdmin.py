from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('kakao_id', 'profile_image', 'real_name', 'phone_number', 'gender', 'birth',)

