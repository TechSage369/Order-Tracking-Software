import logging
from django.conf import settings
from django.db.models import Sum
from billing.models import Order

from .utils import (
    get_present_date,
    get_present_year,
    get_present_month,
    generate_labels_for_month,
    get_total_sales_by_orders,
    make_new_year_range,
    get_week_date_range,

)
from time import perf_counter


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


def get_daily_data(*args, **kwargs):
    # Returns a tuple containing the labels and data
    # for the daily chart
    logger.info('Function Name: get_daily_data')

    start_time = perf_counter()  # start performance timer
    month = get_present_month()
    year = get_present_year()

    if kwargs.get('test'):
        month = kwargs.get('month')
    logger.debug(f'Present Month: {month}')

    orders = Order.objects.filter(
        ordered_on__month=month,
        ordered_on__year=year
    ).values('ordered_on__day').annotate(total_sales=Sum('total_price'))

    label = list(generate_labels_for_month(month))
    data = [0 for i in range(len(label))]

    for order in orders:
        index = label.index(order.get('ordered_on__day'))
        data[index] = order.get('total_sales')

    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    return label, data


def get_weekly_data(*args, **kwargs):
    # Returns a tuple containing the labels and data
    # for the weekly chart
    logger.info('Function Name: get_weekly_data')

    start_time = perf_counter()  # start performance timer
    month = get_present_month()
    year = get_present_year()

    logger.debug(f'Present Month: {month}')
    orders = Order.objects.filter(
        ordered_on__month=month,
        ordered_on__year=year).values('ordered_on__week_day').annotate(total_sales=Sum('total_price'))
    label = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday']
    data = [0 for i in range(len(label))]

    for order in orders:
        index = order.get('ordered_on__week_day') - 1
        data[index] = order.get('total_sales')

    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    return label, data


def get_monthly_data():
    # Returns a tuple containing the labels and data
    # for the monthly chart
    logger.info('Function Name: get_monthly_data')

    start_time = perf_counter()
    year = get_present_year()

    orders = Order.objects.filter(
        ordered_on__year=year,
    ).values('ordered_on__month').annotate(total_sales=Sum("total_price"))

    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
             'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = [0 for i in range(len(label))]

    for order in orders:
        index = order.get('ordered_on__month') - 1
        data[index] = order.get('total_sales')

    if settings.DEBUG:
        logger.info(f'Time Execution: {perf_counter() - start_time}')

    return label, data


def get_yearly_data(*args, **kwargs):
    # Returns a tuple containing the labels and data
    # for the yearly chart
    logger.info('Function Name: get_yearly_data')

    start_time = perf_counter()

    orders = Order.objects.values('ordered_on__year').annotate(
        total_sales=Sum('total_price'))
    label = list(make_new_year_range())
    data = [0 for i in range(len(label))]

    for order in orders:
        index = label.index(order.get('ordered_on__year'))
        data[index] = order.get('total_sales')

    if settings.DEBUG:
        logger.info(f"Execution Time: {perf_counter() - start_time}")

    return label, data


def get_daily_sales(*args, **kwargs):
    # Returns a dictionary containing the daily sales
    logger.info('Function Name: get_daily_sales')
    start_time = perf_counter()
    day = get_present_date().day

    logger.debug(f'Day: {day}')

    # Optional for testing
    if kwargs.get('test'):
        day = kwargs.get('day')

    orders = Order.objects.filter(ordered_on__day=day)

    total_sales = get_total_sales_by_orders(orders)

    if settings.DEBUG:
        logger.info(f"Execution Time: {perf_counter() - start_time}")

    if total_sales == None:
        return 0
    return total_sales


def get_weekly_sales(*args, **kwargs):
    logger.info('Function Name: get_weekly_sales')
    start_time = perf_counter()
    week = get_present_date().weekday() + 1
    start_week_day, end_week_day = get_week_date_range()

    # Optional for testing
    if kwargs.get('test'):
        week = kwargs.get('week')

    orders = Order.objects.filter(
        ordered_on__range=(start_week_day, end_week_day))
    total_sales = get_total_sales_by_orders(orders)

    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    if total_sales == None:
        return 0
    return total_sales


def get_monthly_sales(*args, **kwargs):
    logger.info('Function Name: get_monthly_sales')
    start_time = perf_counter()
    month = get_present_month()

    # Optional for testing
    if kwargs.get('test'):
        month = kwargs.get('month')
        orders = Order.objects.filter(ordered_on__month=month)
        total_sales = get_total_sales_by_orders(orders)
        return total_sales

    orders = Order.objects.filter(ordered_on__month=month)
    total_sales = get_total_sales_by_orders(orders)

    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    if total_sales == None:
        return 0
    return total_sales


def get_yearly_sales(*args, **kwargs):
    logger.info('Function Name: get_yearly_sales')
    start_time = perf_counter()
    year = get_present_year()

    # Optional for testing
    if kwargs.get('test'):
        year = kwargs.get('year')

    orders = Order.objects.filter(ordered_on__year=year)
    total_sales = get_total_sales_by_orders(orders)

    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time  }')

    if total_sales == None:
        return 0
    return total_sales
