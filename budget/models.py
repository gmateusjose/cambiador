from django.db import models
from django.utils import timezone


class Budget(models.Model):
    description = models.CharField(max_length=20)

    def __str__(self):
        return self.description

    def total(self):
        return self.expenses.aggregate(total=models.Sum('amount'))['total']


class BudgetExpense(models.Model):
    budget = models.ForeignKey("budget.Budget", on_delete=models.PROTECT, related_name="expenses")
    description = models.CharField(max_length=20)
    spent_on = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    shared = models.BooleanField(default=False)