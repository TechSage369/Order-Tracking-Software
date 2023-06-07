from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Custom Field to take Month andd year 'MM/YYYY'
'''
NOTE: Use function -> month_year(month: int, year: int) 
It'll set day always to 1 to build custom date 
'''


class MonthYearField(models.DateField):
    # A field to store month and year only (MM/YYYY)

    def validate_month_year(self, value):
        if value.day != 1:
            raise ValidationError(
                "Invalid day specified. Only month/year is allowed.")

    def to_python(self, value):
        value = super().to_python(value)
        self.validate_month_year(value)
        return value

    def get_prep_value(self, value):
        self.validate_month_year(value)
        if value:
            return value.strftime('%m/%Y')
        return value

    def from_db_value(self, value, expression, connection):
        value = super().from_db_value(value, expression, connection)
        self.validate_month_year(value)
        return value


class YearlySale(models.Model):
    year = models.PositiveSmallIntegerField(
        unique=True, primary_key=True, editable=False)
    total_sales = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.year}, Sales: {self.total_sales}"


class MonthlySale(models.Model):
    month_year = MonthYearField(unique=True, editable=False)
    year = models.ForeignKey(
        YearlySale, on_delete=models.CASCADE, editable=False)
    total_sales = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"month: {self.month_year}, Sales: {self.total_sales}"


class DailySale(models.Model):
    date = models.DateField(editable=False, unique=True)
    month = models.ForeignKey(
        MonthlySale, on_delete=models.CASCADE, editable=False)
    total_sales = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.date}, Sales: {self.total_sales}"
