from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models, transaction
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
        average_cost = self.purchases.aggregate(average_cost=models.Avg('usd_price'))['average_cost']
        if average_cost is None:
            average_cost = Decimal('0')
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

    class Meta:
        verbose_name = "Etf Purchase"
        verbose_name_plural = "Etf Purchases"


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


class Exchange(models.Model):
    class Currency(models.TextChoices):
        BRL = 'brl', 'BRL'
        USD = 'usd', 'USD'
        EUR = 'eur', 'EUR'
        BTC = 'btc', 'BTC'
        ETH = 'eth', 'ETH'

    finished_at = models.DateTimeField(default=timezone.now)
    origin = models.CharField(max_length=3, choices=Currency.choices)
    destination = models.CharField(max_length=3, choices=Currency.choices)
    origin_amount = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(0)],
    )
    destination_amount = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(0)],
    )
    def clean(self):
        if self.origin == self.destination:
            raise ValidationError('origin must not be equal to destination')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ExchangeHistory.objects.get_or_create(origin=self.origin, destination=self.destination)


class ExchangeHistory(models.Model):
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Exchange History"
        verbose_name_plural = "Exchange Histories"

    def average_amount(self):
        average_amount = Exchange.objects.filter(
            origin=self.origin,
            destination=self.destination,
        ).annotate(
            relative_amount=models.F('destination_amount')/models.F('origin_amount')
        ).aggregate(
            average_amount=models.Avg('relative_amount')
        )['average_amount']

        if average_amount is None:
            average_amount = Decimal('0')
        return average_amount.quantize(Decimal('1.000000'))
