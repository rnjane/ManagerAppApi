from django.urls import path, include
from . import views

urlpatterns = [
    #User Auth URLs
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.UserSignIn.as_view(), name='signin'),

    #Time budget operations
    path('time-budget/', views.TimeBudgetListCreateView.as_view(), name='time_budget'), #this url covers for creating and viewing all time budgets
    path('time-budget/<int:pk>/', views.TimeBudgetDetails.as_view(), name='time_budget_details'), #this url covers for edit, delete and view single time budget
]