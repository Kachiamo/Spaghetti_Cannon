# Generated by Django 4.2.6 on 2024-01-08 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_models', '0004_tradingmodel_optimal_parameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradingmodel',
            name='model_returns',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tradingmodel',
            name='strategy_returns',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tradingmodel',
            name='symbol_returns',
            field=models.FloatField(blank=True, null=True),
        ),
    ]