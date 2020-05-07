from django.contrib.auth.models import User
from rest_framework import permissions, generics
from . import serializers


class SignUp(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()