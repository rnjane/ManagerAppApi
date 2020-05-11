from django.urls import path, include
from . import views

urlpatterns = [
    #User Auth URLs
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.UserSignIn.as_view(), name='signin'),

    #Time budget operations
    path('time-budget/', views.TimeBudgetModelListCreateView.as_view(), name='time_budget_model'), #this url covers for creating and viewing all time budgets
    path('time-budget/<int:pk>/', views.TimeBudgetModelDetails.as_view(), name='time_budget_model_details'), #this url covers for edit, delete and view single time budget

    #Money budget operations
    path('money-budget/', views.MoneyBudgetModelListCreateView.as_view(), name='money_budget_model'), #this url covers for creating and viewing all money budgets
    path('money-budget/<int:pk>/', views.MoneyBudgetModelDetails.as_view(), name='money_budget_details'), #this url covers for edit, delete and view single money budget

    #Model income operations
    path('model-income/', views.ModelIncomeListCreateView.as_view(), name='model_income_list_create'), #this url covers for creating and viewing all model incomes
    path('model-income/<int:pk>/', views.ModelIncomeDetails.as_view(), name='model_income_details') #this url covers for delete, update and single view of all model incomes
]