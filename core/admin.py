from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class UserMixin:
    """    
    
    """ 
    def activate_users(self, request, queryset):
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, 'Activated {} users.'.format(cnt))
    activate_users.short_description = 'Activate Users'  # type: ignore

class CustomUserAdmin(UserAdmin, UserMixin):
    list_display = [
        'username',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined',
    ]
    list_editable = (
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined',
    )
    list_display_links =('username',)
    actions = [
        'activate_users',
    ]

    def settings_time_zone(self, instance):
        """
        This method allows us to access the time_zone attribute of Settings
        to display in the Django Admin.
        """
        return instance.settings.time_zone
    settings_time_zone.short_description = 'Time zone'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
