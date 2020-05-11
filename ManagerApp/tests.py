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


class TimeBudgetModelTestCase(BaseViewTest):
    def test_user_can_create_a_time_budget(self):
        response = self.client.post(reverse('time_budget_model'), {'time_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_view_all_time_budgets(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user, _quantity=10)
        response = self.client.get(reverse('time_budget_model'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_user_can_view_a_time_budget(self):
        mommy.make(models.TimeBudgetModel, time_budget_name='testmodelbudget', owner=self.testing_user)
        response = self.client.get(reverse('time_budget_model_details', kwargs={'pk': 1}))
        self.assertEqual('testmodelbudget', response.data['time_budget_name'])

    def test_user_can_update_a_time_budget(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = self.client.patch(reverse('time_budget_model_details', kwargs={'pk': 1}), {'time_budget_name': 'new time budget name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new time budget name', response.data['time_budget_name'])

    def test_user_can_delete_a_budget(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = self.client.delete(reverse('time_budget_model_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_time_budget_operations_require_authentication(self):
        client2 = APIClient()
        response = client2.post(reverse('time_budget_model'), {'time_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_time_budget_operations_require_authorisation(self):
        mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = self.client2.get(reverse('time_budget_model_details', kwargs={'pk': 1}))
        response2 = self.client.get(reverse('time_budget_model_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class MonetaryBudgetModelTestCase(BaseViewTest):
    def test_user_can_create_a_money_budget(self):
        response = self.client.post(reverse('money_budget_model'), {'money_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_view_all_money_budgets(self):
        mommy.make(models.MoneyBudgetModel, owner=self.testing_user, _quantity=10)
        response = self.client.get(reverse('money_budget_model'))
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
        response = client2.post(reverse('money_budget_model'), {'money_budget_name': 'testtimebudget'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_money_budget_operations_require_authorisation(self):
        mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        response = self.client2.get(reverse('money_budget_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response2 = self.client.get(reverse('money_budget_details', kwargs={'pk': 1}))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class TestMoneyBudgetModelIncome(BaseViewTest):
    def test_user_can_create_model_income(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        model_income_response = self.client.post(reverse('model_income_list_create'), {'model_income_name': 'test model income', 'model_budget': model_budget.id, 'owner':self.testing_user})
        self.assertEqual(model_income_response.status_code, status.HTTP_201_CREATED)
        

    def test_user_can_view_all_model_incomes(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        mommy.make(models.ModelIncome, owner=self.testing_user, model_budget = model_budget, _quantity=10)
        model_income_view_response = self.client.get(reverse('model_income_list_create'))
        self.assertEqual(model_income_view_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(model_income_view_response.data), 10)

    def test_user_can_update_a_model_income(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        mommy.make(models.ModelIncome, owner=self.testing_user, model_budget = model_budget, _quantity=10)
        response = self.client.patch(reverse('model_income_details', kwargs={'pk': 1}), {'model_income_name': 'new model income name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new model income name', response.data['model_income_name'])

    def test_user_can_delete_a_model_income(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        mommy.make(models.ModelIncome, owner=self.testing_user, model_budget = model_budget)
        response = self.client.delete(reverse('model_income_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_model_income_operations_require_authentication(self):
        client2 = APIClient()
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        response = client2.post(reverse('model_income_list_create'), {'model_income_name': 'test model income', 'model_budget': model_budget.id, 'owner':self.testing_user})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_money_budget_operations_require_authorisation(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        model_income = mommy.make(models.ModelIncome, owner=self.testing_user, model_budget = model_budget)
        response = self.client2.get(reverse('model_income_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response2 = self.client.get(reverse('model_income_details', kwargs={'pk': 1}))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class TestMoneyBudgetModelExpense(BaseViewTest):
    def test_user_can_create_model_expense(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        model_expense_response = self.client.post(reverse('model_expense_list_create'), {'model_expense_name': 'test model expense', 'model_budget': model_budget.id, 'owner':self.testing_user})
        self.assertEqual(model_expense_response.status_code, status.HTTP_201_CREATED)
        

    def test_user_can_view_all_model_expenses(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        mommy.make(models.ModelExpense, owner=self.testing_user, model_budget = model_budget, _quantity=10)
        model_expense_view_response = self.client.get(reverse('model_expense_list_create'))
        self.assertEqual(model_expense_view_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(model_expense_view_response.data), 10)

    def test_user_can_update_a_model_expense(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        mommy.make(models.ModelExpense, owner=self.testing_user, model_budget = model_budget)
        response = self.client.patch(reverse('model_expense_details', kwargs={'pk': 1}), {'model_expense_name': 'new model expense name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new model expense name', response.data['model_expense_name'])

    def test_user_can_delete_a_model_expense(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        mommy.make(models.ModelExpense, owner=self.testing_user, model_budget = model_budget)
        response = self.client.delete(reverse('model_expense_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_model_expense_operations_require_authentication(self):
        client2 = APIClient()
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        response = client2.post(reverse('model_expense_list_create'), {'model_expense_name': 'test model expense', 'model_budget': model_budget.id, 'owner':self.testing_user})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_money_budget_operations_require_authorisation(self):
        model_budget = mommy.make(models.MoneyBudgetModel, owner=self.testing_user)
        model_expense = mommy.make(models.ModelExpense, owner=self.testing_user, model_budget = model_budget)
        response = self.client2.get(reverse('model_expense_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response2 = self.client.get(reverse('model_expense_details', kwargs={'pk': 1}))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class TestTimeSlotModel(BaseViewTest):
    def test_user_can_create_a_time_slot_model(self):
        model_time_budget = mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = self.client.post(reverse('time_slot_model_list_create'), {'time_slot_name': 'test time slot model', 'model_time_budget': model_time_budget.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

    def test_user_can_view_all_time_slot_models(self):
        model_time_budget = mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        mommy.make(models.TimeSlotModel, owner=self.testing_user, model_time_budget = model_time_budget, _quantity=10)
        response = self.client.get(reverse('time_slot_model_list_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_user_can_update_a_model_expense(self):
        model_time_budget = mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        mommy.make(models.TimeSlotModel, owner=self.testing_user, model_time_budget=model_time_budget)
        response = self.client.patch(reverse('time_slot_model_details', kwargs={'pk': 1}), {'time_slot_name': 'new model time slot name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('new model time slot name', response.data['time_slot_name'])

    def test_user_can_delete_a_model_time_slot(self):
        model_time_budget = mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        mommy.make(models.TimeSlotModel, owner=self.testing_user, model_time_budget=model_time_budget)
        response = self.client.delete(reverse('time_slot_model_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_model_expense_operations_require_authentication(self):
        client2 = APIClient()
        model_time_budget = mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        response = client2.post(reverse('time_slot_model_list_create'), {'time_slot_name': 'test model time slot', 'model_time_budget': model_time_budget.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_money_budget_operations_require_authorisation(self):
        model_time_budget = mommy.make(models.TimeBudgetModel, owner=self.testing_user)
        model_time_slot = mommy.make(models.TimeSlotModel, owner=self.testing_user, model_time_budget=model_time_budget)
        response = self.client2.get(reverse('time_slot_model_details', kwargs={'pk': 1}))
        response2 = self.client.get(reverse('time_slot_model_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class UserBudgetsTests(BaseViewTest):
    def test_user_can_create_a_budget(self):
        pass

    def test_new_budget_follows_current_model(self):
        pass

    def test_user_can_mark_budget_model_active(self):
        pass