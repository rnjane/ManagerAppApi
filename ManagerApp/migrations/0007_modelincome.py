# Generated by Django 3.0.6 on 2020-05-08 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerApp', '0006_auto_20200508_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('model_income_name', models.CharField(max_length=50, verbose_name='Model Income Name')),
                ('budget_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ManagerApp.MoneyBudgetModel', verbose_name='Budget Model')),
            ],
            options={
                'verbose_name': 'Model Income',
                'verbose_name_plural': 'Model Income',
                'ordering': ['date_created'],
            },
        ),
    ]
