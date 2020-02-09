import logging

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from timezone_field import TimeZoneField

from core.models import TimeStampedModel

logger = logging.getLogger(__name__)

class UserSettings(TimeStampedModel):
    """
    Model to store additional user settings and preferences. Extends User
    model.
    """
    user = models.OneToOneField(User, related_name='settings',on_delete=models.CASCADE,)
    organization = models.CharField("Institution/Organization",max_length=150, blank=True, null=True)
    # time_zone = TimeZoneField(default=settings.TIME_ZONE)

    def username(self):
        return self.user.username
    username.admin_order_field = 'user__username'

    @receiver(post_save, sender=User)
    def create_usersettings_on_user_create(sender, **kwargs):
        """
        Automatically create a UserSettings object when a new user is created.
        """
        instance = kwargs['instance']

        if kwargs.get('created', True):
            UserSettings.objects.get_or_create(user=instance)
            
    class Meta:
        verbose_name_plural = 'User Settings'

