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
    path('model-income/<int:pk>/', views.ModelIncomeDetails.as_view(), name='model_income_details'), #this url covers for delete, update and single view of all model incomes

    #Model expense operations
    path('model-expense/', views.ModelExpenseListCreateView.as_view(), name='model_expense_list_create'), #this url covers for creating and viewing all model expenses
    path('model-expense/<int:pk>/', views.ModelExpenseDetails.as_view(), name='model_expense_details'), #this url covers for delete, update and single view of all model expenses

    #time slot model urls
    path('time-slot-model/', views.TimeSlotModelListCreate.as_view(), name='time_slot_model_list_create'),
    path('time-slot-model/<int:pk>/', views.TimeSlotModelDetails.as_view(), name='time_slot_model_details'),

    #budgets urls
    path('budgets/', views.BudgetsListCreate.as_view(), name='budgets'),
    path('budget-details/<int:pk>/', views.BudgetDetails.as_view(), name='budget_details'),

    #budget incomes & expenses
    path('budget-income/', views.BudgetIncome.as_view(), name='budget_income'),
    path('budget-income-details/', views.BudgetIncomeDetails.as_view(), name='budget_income_details'),
    path('budget-expense/', views.BudgetExpense.as_view(), name='budget_expense'),
    path('budget-expense-details/', views.BudgetExpenseDetails.as_view(), name='budget_expense_details'),

    #income & expenses categories
    path('income-categories/', views.IncomeCategories.as_view(), name='income_categories'),
    path('expense-categories/', views.ExpenseCategories.as_view(), name='expense_categories')
]