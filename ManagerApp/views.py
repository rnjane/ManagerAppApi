from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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


class TimeBudgetModelListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.TimeBudgetModelSerializer
    queryset = models.TimeBudgetModel.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TimeBudgetModelDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.TimeBudgetModelSerializer
    queryset = models.TimeBudgetModel.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class MoneyBudgetModelListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.MoneyBudgetModelSerializer
    queryset = models.MoneyBudgetModel.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MoneyBudgetModelDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.MoneyBudgetModelSerializer
    queryset = models.MoneyBudgetModel.objects.filter()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class ModelIncomeListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ModelIncomeSerializer
    queryset = models.ModelIncome.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class ModelIncomeDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ModelIncomeSerializer
    queryset = models.ModelIncome.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class ModelExpenseListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ModelExpenseSerializer
    queryset = models.ModelExpense.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class ModelExpenseDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ModelExpenseSerializer
    queryset = models.ModelExpense.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class TimeSlotModelListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.TimeSlotModelSerializer
    queryset = models.TimeSlotModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

class TimeSlotModelDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.TimeSlotModelSerializer
    queryset = models.TimeSlotModel.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset