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
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    morningstar_rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    def __str__(self):
        return f"{self.ticker}"

    def average_usd_cost(self):
        data = self.purchases.aggregate(average_cost=models.Avg('usd_price'))
        return Decimal(data['average_cost']).quantize(Decimal('1.00'))


class Purchase(models.Model):
    etf = models.ForeignKey("investment.Etf", on_delete=models.PROTECT, related_name="purchases")
    purchased_at = models.DateTimeField(default=timezone.now)
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
