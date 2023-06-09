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

    data = Order.objects.all()
    print("Initializing all Order")

    progress_bar = tqdm(total=len(
        data), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{percentage:3.0f}%]')

    for obj in data:
        x = obj
        obj.save()
        progress_bar.update(1)
    progress_bar.close()
    print(f"Completed: {perf_counter()-start_time}s")
