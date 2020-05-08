from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions, generics, response, status, authtoken, views
from . import serializers, models, permisions


class SignUp(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class UserSignIn(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                return response.Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)
            else:
                token, _ = authtoken.models.Token.objects.get_or_create(user=user)
                return response.Response({'token': token.key},
                status=status.HTTP_200_OK)
        return response.Response({'token': token.key},
                status=status.HTTP_400_BAD_REQUEST)


class TimeBudgetListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, permisions.AllowOwnerOnly)
    serializer_class = serializers.TimeBudgetSerializer
    queryset = models.TimeBudgetModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TimeBudgetDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permisions.AllowOwnerOnly)
    serializer_class = serializers.TimeBudgetSerializer
    queryset = models.TimeBudgetModel.objects.all()


class MoneyBudgetListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, permisions.AllowOwnerOnly)
    serializer_class = serializers.MoneyBudgetSerializer
    queryset = models.MoneyBudgetModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MoneyBudgetDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permisions.AllowOwnerOnly)
    serializer_class = serializers.MoneyBudgetSerializer
    queryset = models.MoneyBudgetModel.objects.all()