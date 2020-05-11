import re
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", validated_data['email']):
            raise ValidationError("Enter a valid email address.")
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', validated_data['password']):
            raise ValidationError("Enter a valid password. Password should be at least 8 characters long.")

        username = validated_data.get('username', None)
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        if username and email and password:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        raise(serializers.ValidationError('Please provide username, email, password and password confirmation'))


class TimeBudgetModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = models.TimeBudgetModel
        fields = ['owner', 'time_budget_name']

class MoneyBudgetModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    model_incomes = serializers.StringRelatedField(read_only=True, many=True)
    model_expenses = serializers.StringRelatedField(read_only=True, many=True)
    
    class Meta:
        model = models.MoneyBudgetModel
        fields = ['owner', 'money_budget_name', 'model_incomes', 'model_expenses']


class ModelIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelIncome
        fields = ['model_budget', 'model_income_name']


class ModelExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelExpense
        fields = ['model_budget', 'model_expense_name']


class TimeSlotModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TimeSlotModel
        fields = ['time_slot_name', 'model_time_budget']


class BudgetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    incomes = serializers.StringRelatedField(read_only=True, many=True)
    expenses = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = models.Budget
        fields = ['budget_name', 'owner', 'budget_model', 'incomes', 'expenses']


class BudgetExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BudgetExpense
        fields = ('name', 'amount', 'category', 'description', 'date_created', 'budget')


class BudgetIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BudgetIncome
        fields = ('name', 'amount', 'category', 'description', 'date_created', 'budget')