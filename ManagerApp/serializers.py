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
    class Meta:
        model = models.MoneyBudgetModel
        fields = ['owner', 'money_budget_name']