# Generated by Django 3.0.6 on 2020-05-11 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ManagerApp', '0014_modelexpense'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlotModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('time_slot_name', models.CharField(max_length=50, verbose_name='Time Slot Model Name')),
                ('model_time_budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_slot_models', to='ManagerApp.TimeBudgetModel', verbose_name='Time Slot Model')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_slot_model', to=settings.AUTH_USER_MODEL, verbose_name='Time Slot Model Owner')),
            ],
            options={
                'verbose_name': 'Time slot model',
                'verbose_name_plural': 'Time Slot Model',
                'ordering': ['date_created'],
            },
        ),
    ]