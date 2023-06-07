import datetime
import calendar
import random
import logging
from billing.models import Item, Order, OrderItem
from django.conf import settings
from django.db.models import Sum


LOG_DIR = settings.BASE_DIR / 'logs'
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*2,
            'backupCount': 10,
            'formatter': 'file',
            'filename': f'{LOG_DIR}/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logger = logging.getLogger(__name__)


def get_present_date():
    # Returns current datetimeobj in ist timezone
    return datetime.datetime.now()


def get_present_month():
    # returns present month
    return get_present_date().month


def get_present_day():
    return get_present_date().weekday()


def get_present_year():
    return get_present_date().year


def get_total_sales_by_orders(orders):
    # Returns total sales of the orders
    return orders.aggregate(total_sales=Sum('total_price'))['total_sales']


def generate_labels_for_month(month: int):
    # generates labels for month
    logger.info('Function Name: generate_labels_for_month')
    month = get_present_month()
    year = get_present_year()
    number_of_days = calendar.monthrange(year, month)[1]
    return range(1, number_of_days+1)


def get_random_date():
    # Returns random date
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)


def generate_dummy_daily_orders(limit_per_day=50):
    # Returns dummy daily orders data
    items = Item.objects.all()
    for i in range(1, 31):
        random_limit_per_day = random.randint(1, limit_per_day)
        for j in range(random_limit_per_day):
            order = Order.objects.create(
                ordered_on=datetime.date(2021, 1, i),
                order_status="Paid"
            )
            item = random.choice(items)
            order_item = OrderItem.objects.create(
                order=order,
                item=item,
                quantity=random.randint(1, 5)
            )
            order_item.save()
            order.is_new = False
            order.save()
            print(
                f'Day: {i} Order: {j} LimitPerDay: {random_limit_per_day} Created', end="\r")


def generate_dummy_orders(limit=100):
    # Returns dummy orders data
    items = Item.objects.all()
    item_limit = random.randint(1, 8)
    for i in range(limit):
        order = Order.objects.create(
            pk=i,
            ordered_on=get_random_date(),
            order_status="Paid"
        )
        for j in range(item_limit):
            item = random.choice(items)
            order_item = OrderItem.objects.create(
                order=order,
                item=item,
                quantity=random.randint(1, 5)
            )
            order_item.save()
            order.is_new = False
            order.save()
            print(
                f'Order {i} Item {j} Created|Order.isNew={order.is_new}', end="\r")


def get_min_max_year():
    # Returns a tuple containing the min and max year
    # to be used while rendering the statistics page
    CURRENT_YEAR = get_present_year()
    remainder = CURRENT_YEAR % 10
    min_year = CURRENT_YEAR - remainder
    max_year = min_year + 10
    return min_year, max_year


def make_new_year_range():
    # Returns a generator range object for the range of years
    # to be used while rendering the statistics page
    min_year, max_year = get_min_max_year()
    return range(min_year, max_year+1)


def get_week_date_range():
    current_date = get_present_date()
    week = current_date.weekday()
    start_date = current_date - datetime.timedelta(days=week)
    return start_date, current_date


# It is specifically build for making days to always 1
# to make custom field for MM/YYYY
def month_year(date) -> datetime.date:
    new_date = datetime.date(date.year, date.month, 1)
    return new_date
