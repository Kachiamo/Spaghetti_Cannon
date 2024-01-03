from django.db import models


class Stock(models.Model):
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    symbol = models.CharField(primary_key=True, max_length=6)
    name = models.TextField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    ipo_year = models.PositiveSmallIntegerField(blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
