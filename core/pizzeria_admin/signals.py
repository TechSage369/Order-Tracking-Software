from django.db.models.signals import post_save, pre_delete
from django.db.models import Q
from django.dispatch import receiver
from billing.models import Order
from .models import DailySale, MonthlySale, YearlySale
import datetime
from . import utils


@receiver(post_save, sender=Order)
@receiver(pre_delete, sender=Order)
def calculate_total(sender, instance, **kwargs):
    # print(f"_____Calculating Daily Sales____________{instance.ordered_on}")
    daily_sales(instance.ordered_on.date())


def daily_sales(date):
    orders = Order.objects.filter(ordered_on__date=date)
    try:
        obj = DailySale.objects.get(date=date)
        obj.total_sales = sum(order.total_price for order in orders)
        obj.save()
        monthly_sales(date)

    except Exception as e:
        # print(f"Warning: {e}")
        create_day(date)
        daily_sales(date)


def monthly_sales(date):
    sales = DailySale.objects.filter(
        Q(date__month=date.month) & Q(date__year=date.year))
    try:
        obj = MonthlySale.objects.get(month_year=utils.month_year(date))
        obj.total_sales = sum(sale.total_sales for sale in sales)
        obj.save()
        yearly_sales(date.year)
    except Exception as e:
        print(f"Warning: monthly_sales {e}")
        create_month(date)
        monthly_sales()


def yearly_sales(year):
    sales = MonthlySale.objects.filter(month_year__year=year)
    try:
        obj = YearlySale.objects.get(year=year)
        obj.total_sales = sum(sale.total_sales for sale in sales)
        obj.save()
    except Exception as e:
        # print(f"_____________________________-Warning: Yearly_sales {e}")
        create_year(year)
        yearly_sales(year)


def create_day(date, *args, **kwargs):
    month = date.month
    try:
        month = MonthlySale.objects.get(month_year=utils.month_year(date))
        obj = DailySale(date=date, month=month)
        obj.save()
    except:
        create_month(date)
        create_day(date)


def create_month(date, **kwargs):
    try:
        year = YearlySale.objects.get(year=date.year)
        obj = MonthlySale(month_year=date, year=year)
        obj.save()
    except:
        create_year(date.year)
        create_month(date)


def create_year(year, *args, **kwargs):
    obj = YearlySale(year=year)
    obj.save()
