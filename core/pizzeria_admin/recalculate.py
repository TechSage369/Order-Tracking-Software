from billing.models import Order
from tqdm import tqdm
from pizzeria_admin.models import DailySale, YearlySale, MonthlySale
from time import perf_counter


def calculate():
    start_time = perf_counter()
    print("____Removing All sales cache_____")
    DailySale.objects.all().delete()
    YearlySale.objects.all().delete()
    MonthlySale.objects.all().delete()

    print("Initializing all Order")
    distinct_dates = Order.objects.values_list(
        'ordered_on__date', flat=True).distinct()
    progress_bar = tqdm(total=len(
        distinct_dates), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{percentage:3.0f}%]')

    for date in distinct_dates:
        order_objects = Order.objects.filter(ordered_on__date=date)
        obj = order_objects[0]
        obj.save()
        progress_bar.update(1)
    progress_bar.close()
    print(f"Completed: {perf_counter()-start_time}s")
