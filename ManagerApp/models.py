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
    time_budget_owner = models.ForeignKey(User, related_name='timebudget', verbose_name=_("Time Budget Owner"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Time Budget")
        verbose_name_plural = _("Time Budgets")
        ordering = ['date_created']

    def __str__(self):
        return self.time_budget_name

    def get_absolute_url(self):
        return reverse("time_budget_detail", kwargs={"pk": self.pk})