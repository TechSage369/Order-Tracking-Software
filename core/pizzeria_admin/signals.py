from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from billing.models import Order
from .models import DailySale, MonthlySale, YearlySale
from datetime import date


@receiver(post_save, sender=Order)
@receiver(post_delete, sender=Order)
def calculate_total(sender, instance, **kwargs):
    print(
        f"_____________________Called Calculate Total Techsage: {instance.ordered_on.month}")
    print(f"Ordered On: {instance.ordered_on.date()}")
    daily_sells(instance.ordered_on.date())


def daily_sells(date):
    orders = Order.objects.filter(ordered_on__date=date)
    day = DailySale.objects.get_or_create(date=date)
    if not day:
        create_day(date)
    obj = DailySale.objects.get(date=date)
    total = sum(order.total_price for order in orders)
    obj.total_sales = total
    obj.save()


def create_day(date, *args, **kwargs):
    month = date.month
    year = date.year
    check_month = MonthlySale.objects.filter(month=month, year=year).exists()
    if not check_month:
        create_month(month, year)

    obj, created = DailySale.objects.get_or_create(date=date, month=month)
    if not created:
        obj.save()


def create_month(month, year, **kwargs):
    check_year = YearlySale.objects.filter(year=year).exists()
    if not check_year:
        create_year(year)
    obj, created = MonthlySale.objects.get_or_create(month=month, year=year)
    if not created:
        obj.save()


def create_year(year, *args, **kwargs):
    obj = YearlySale.objects.get_or_create(year=year)
