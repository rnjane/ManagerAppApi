# Generated by Django 3.0.6 on 2020-05-07 20:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ManagerApp', '0002_auto_20200507_2038'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TimeBudget',
            new_name='TimeBudgetModel',
        ),
    ]
