# Generated by Django 3.0.6 on 2020-05-07 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timebudget',
            old_name='owner',
            new_name='time_budget_owner',
        ),
    ]
