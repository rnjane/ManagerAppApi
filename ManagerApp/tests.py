from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from . import models


class BaseViewTest(APITestCase):
    def setUp(self):
        client = APIClient()
        client.post(reverse('signup'), {'username': 'testuser1', 'email': 'test@test.com', 'password': 'testpass'})
        self.testing_user = User.objects.get(username='testuser1')
        self.token = Token.objects.create(user=self.testing_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.client2 = APIClient()
        self.client2.post(reverse('signup'), {'username': 'testuser2', 'email': 'test2@test.com', 'password': 'testpass'})
        self.token2 = Token.objects.create(user=User.objects.get(username='testuser2'))
        self.client2.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)

class UsersTestCase(BaseViewTest):
    def test_user_signup(self):
        response = self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_signup_needs_all_arguments(self):
        response = self.client.post(reverse('signup'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_should_be_singular(self):
        self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass'})
        response = self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test@test.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_or_password(self):
        response = self.client.post(reverse('signup'), {'username': 'testuser', 'email': 'test', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_user_can_login(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser1', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_credentials_cant_login(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser1', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TimeBudgetsTestCase(BaseViewTest):
    def test_user_can_create_a_time_budget(self):
        response = self.client.post(reverse('time_budget'), {'time_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_view_all_time_budgets(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user, _quantity=10)
        response = self.client.get(reverse('time_budget'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_user_can_view_a_time_budget(self):
        mommy.make(models.TimeBudgetModel, time_budget_name='testmodelbudget', owner=self.testing_user)
        response = self.client.get(reverse('time_budget_details', kwargs={'pk': 1}))
        self.assertEqual('testmodelbudget', response.data['time_budget_name'])

    def test_user_can_update_a_time_budget(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = self.client.patch(reverse('time_budget_details', kwargs={'pk': 1}), {'time_budget_name': 'new time budget name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new time budget name', response.data['time_budget_name'])

    def test_user_can_delete_a_budget(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = self.client.delete(reverse('time_budget_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_time_budget_operations_require_authentication(self):
        client2 = APIClient()
        response = client2.post(reverse('time_budget'), {'time_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_time_budget_operations_require_authorisation(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = self.client2.get(reverse('time_budget_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MonetaryBudgetsTestCase(BaseViewTest):
    def test_user_can_create_a_money_budget(self):
        response = self.client.post(reverse('money_budget'), {'money_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_view_all_money_budgets(self):
        mommy.make(models.MoneyBudgetModel, owner=self.testing_user, _quantity=10)
        response = self.client.get(reverse('money_budget'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_user_can_view_a_money_budget(self):
        mommy.make(models.MoneyBudgetModel, money_budget_name='testmodelbudget', owner=self.testing_user)
        response = self.client.get(reverse('money_budget_details', kwargs={'pk': 1}))
        self.assertEqual('testmodelbudget', response.data['money_budget_name'])

    def test_user_can_update_a_money_budget(self):
        mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        response = self.client.patch(reverse('money_budget_details', kwargs={'pk': 1}), {'money_budget_name': 'new money budget name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new money budget name', response.data['money_budget_name'])

    def test_user_can_delete_a_money_budget(self):
        mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        response = self.client.delete(reverse('money_budget_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_money_budget_operations_require_authentication(self):
        client2 = APIClient()
        response = client2.post(reverse('money_budget'), {'money_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_money_budget_operations_require_authorisation(self):
        mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        response = self.client2.get(reverse('money_budget_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)