from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeBudgetModel(BaseModel):
    time_budget_name = models.CharField(_("Time Budget Name"), max_length=50)
    owner = models.ForeignKey(User, related_name='timebudget', verbose_name=_("Time Budget Owner"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Time Budget")
        verbose_name_plural = _("Time Budgets")
        ordering = ['date_created']

    def __str__(self):
        return self.time_budget_name

    def get_absolute_url(self):
        return reverse("time_budget_detail", kwargs={"pk": self.pk})


class MoneyBudgetModel(BaseModel):
    money_budget_name = models.CharField(_("Money Budget Name"), max_length=50)
    owner = models.ForeignKey(User, related_name='moneybudget', verbose_name=_("Money Budget Owner"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Money Budget")
        verbose_name_plural = _("Money Budgets")
        ordering = ['date_created']

    def __str__(self):
        return self.money_budget_name

    def get_absolute_url(self):
        return reverse("money_budget_detail", kwargs={"pk": self.pk})