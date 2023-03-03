# Generated by Django 4.0.4 on 2023-03-03 20:11

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0003_alter_etf_sharpe_ratio_3yr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('origin', models.CharField(choices=[('brl', 'BRL'), ('usd', 'USD'), ('eur', 'EUR'), ('btc', 'BTC'), ('eth', 'ETH')], max_length=3)),
                ('destination', models.CharField(choices=[('brl', 'BRL'), ('usd', 'USD'), ('eur', 'EUR'), ('btc', 'BTC'), ('eth', 'ETH')], max_length=3)),
                ('origin_amount', models.DecimalField(decimal_places=6, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('destination_amount', models.DecimalField(decimal_places=6, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=3)),
                ('destination', models.CharField(max_length=3)),
            ],
        ),
    ]
