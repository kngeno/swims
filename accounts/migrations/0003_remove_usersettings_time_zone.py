# Generated by Django 2.2.5 on 2019-11-07 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_usersettings_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='time_zone',
        ),
    ]
