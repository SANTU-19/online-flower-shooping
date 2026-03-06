from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'full_name',
        'phone',
        'is_email_verified',
        'account_created',
        'last_login_time',
    )

    search_fields = ('user__username', 'full_name', 'phone')
    list_filter = ('is_email_verified',)
    list_editable = ('phone',)

    def account_created(self, obj):
        return obj.user.date_joined

    account_created.short_description = "Account Created"

    def last_login_time(self, obj):
        return obj.user.last_login

    last_login_time.short_description = "Last Login"