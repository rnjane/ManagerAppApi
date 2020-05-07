# Generated by Django 3.0.6 on 2020-05-07 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ManagerApp', '0003_auto_20200507_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timebudgetmodel',
            name='time_budget_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TimeBudget', to=settings.AUTH_USER_MODEL, verbose_name='Time Budget Owner'),
        ),
    ]
