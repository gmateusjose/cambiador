from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Etf(models.Model):
    ticker = models.CharField(max_length=5, primary_key=True)
    expense_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    annual_yield = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    sharpe_ratio_3yr = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        validators=[MinValueValidator(-1), MaxValueValidator(1)],
    )
    morningstar_rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    def __str__(self):
        return f"{self.ticker}"

    def average_usd_cost(self):
        average_cost = Decimal('0')
        data = self.purchases.aggregate(average_cost=models.Avg('usd_price'))
        if data['average_cost'] is not None:
            average_cost = Decimal(data['average_cost'])
        return average_cost.quantize(Decimal('1.00'))


class Purchase(models.Model):
    purchased_at = models.DateTimeField(default=timezone.now)
    etf = models.ForeignKey(
        "investment.Etf",
        on_delete=models.PROTECT,
        related_name="purchases",
    )
    usd_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )


class Dividend(models.Model):
    received_at = models.DateTimeField(default=timezone.now)
    raw_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    net_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )


# class Currency(models.Model):
#     name = models.CharField(max_length=10, primary_key=True)

#     def __str__(self):
#         return f"{self.name}"

#     def average_cost(self):
#         average_cost = Decimal('0')
#         data = self.purchases.aggregate(average_cost=models.Avg('brl_price'))
#         if data['average_cost'] is not None:
#             average_cost = Decimal(data['average_cost'])
#         return average_cost.quantize(Decimal('1.00'))


# class CurrencyPurchase(models.Model):
#     purchased_at = models.DateTimeField(default=timezone.now)
#     currency = models.ForeignKey(
#         "investment.Currency",
#         on_delete=models.PROTECT,
#         related_name="purchases"
#     )
#     brl_price = models.DecimalField(
#         max_digits=8,
#         decimal_places=2,
#         validators=[MinValueValidator(0)],
#     )