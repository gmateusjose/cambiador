# Generated by Django 4.0.4 on 2023-02-28 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='etf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchases', to='investment.etf'),
        ),
    ]
