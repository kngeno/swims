from django.contrib import admin

from accounts.models import UserSettings


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'organization',
        'modified',
        'created',
    ]
    list_editable = (
        'organization',
    )
    list_display_links =('username',)

admin.site.register(UserSettings, UserSettingsAdmin)
