from typing import Iterable, Optional
from django.db import models
import datetime
from . import utils
from django.utils.translation import gettext_lazy as _

# Custom Field to take Month andd year 'MM/YYYY'
'''
NOTE: Use function -> month_year(month: int, year: int) 
It'll set day always to 1 to build custom date 
'''


class YearlySale(models.Model):
    year = models.PositiveSmallIntegerField(
        unique=True, primary_key=True, editable=False)
    total_sales = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.year}, Sales: {self.total_sales}"


class MonthlySale(models.Model):
    month_year = models.DateField(unique=True, editable=False)
    year = models.ForeignKey(
        YearlySale, on_delete=models.CASCADE, editable=False)
    total_sales = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.month_year = utils.month_year(self.month_year)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"month: {self.month_year}, Sales: {self.total_sales}"


class DailySale(models.Model):
    date = models.DateField(editable=False, unique=True)
    month = models.ForeignKey(
        MonthlySale, on_delete=models.CASCADE, editable=False)
    total_sales = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.date}, Sales: {self.total_sales}"
