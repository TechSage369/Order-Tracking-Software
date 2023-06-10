import random
import datetime
from time import perf_counter
from billing.models import Order, Item


def create_dummy_orders_optimization(limit=100, item_limit=8):
    # Returns dummy orders data
    items = Item.objects.all()
    item_limit = random.randint(1, item_limit)
    for i in range(limit):
        order = Order.objects.create(order_status="Paid")
        for j in range(item_limit):
            item = random.choice(items)
            order.items.add(item)
            order.is_new = False
            order.is_paid = True
            order.save()
        order.total_price = order.get_total_price()
        order.save()
        print(f'Order: {i} | Percentage: {round(i/limit*100, 2)}%', end="\r")


def check_performance(func, *args, **kwargs):
    # Returns the execution time of a function
    start_time = perf_counter()
    func(*args, **kwargs)
    return perf_counter() - start_time


def get_custom_date(year=2021, month=1, day=1):
    return datetime.datetime(year, month, day)
