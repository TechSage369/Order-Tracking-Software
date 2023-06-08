import logging
from django.conf import settings
from django.db.models import Sum, Q
from billing.models import Order
from .models import DailySale, MonthlySale, YearlySale

from .utils import (
    get_present_date,
    get_present_year,
    get_present_month,
    generate_labels_for_month,
    get_total_sales_by_orders,
    make_new_year_range,
    get_week_date_range,
    get_day_dict,
    month_year,
    generate_date_dictionary,

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
    # Returns a list containing the labels and data
    # for the daily chart
    logger.info('Function Name: get_daily_data')

    start_time = perf_counter()  # start performance timer

    date = get_present_date().date()
    sales = DailySale.objects.filter(
        Q(date__month=date.month) & Q(date__year=date.year))

    month_dict = get_day_dict(date.year, date.month)

    for sale in sales:
        key = sale.date.day
        month_dict[key] = sale.total_sales

    label = list(month_dict.keys())
    data = list(month_dict.values())
    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    return label, data


def get_weekly_data(*args, **kwargs):
    # Returns a tuple containing the labels and data
    # for the weekly chart
    logger.info('Function Name: get_weekly_data')

    start_time = perf_counter()  # start performance timer
    week_range = get_week_date_range(get_present_date().date())
    w_dict = generate_date_dictionary(week_range[0], week_range[1])

    week_sales = DailySale.objects.filter(
        Q(date__range=(week_range[0], week_range[1])))

    label = ['Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday',]

    for sales in week_sales:
        key = sales.date
        w_dict[key] = sales.total_sales
    data = list(w_dict.values())
    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    return label, data


def get_monthly_data():
    # Returns a tuple containing the labels and data
    # for the monthly chart
    logger.info('Function Name: get_monthly_data')

    start_time = perf_counter()
    year = get_present_year()
    monthly_data = MonthlySale.objects.filter(year=year)

    month_dict = dict.fromkeys(range(1, 12 + 1), 0)
    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
             'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for d in monthly_data:
        key = d.month_year.month
        month_dict[key] = d.total_sales
    data = list(month_dict.values())
    if settings.DEBUG:
        logger.info(f'Time Execution: {perf_counter() - start_time}')

    return label, data


def get_yearly_data(*args, **kwargs):
    # Returns a tuple containing the labels and data
    # for the yearly chart
    logger.info('Function Name: get_yearly_data')

    start_time = perf_counter()
    obj = YearlySale.objects.all()
    yrs = [x.year for x in obj]

    year_min = min(yrs)
    year_max = max(yrs)

    if (year_max - year_min) < 10:
        while (year_max - year_min) < 10:
            year_max += 1

    year_dict = dict.fromkeys(range(year_min, (year_max + 1)), 0)

    for y in obj:
        key = y.year
        year_dict[key] = y.total_sales

    if settings.DEBUG:
        logger.info(f"Execution Time: {perf_counter() - start_time}")
    data = list(year_dict.values())
    label = list(year_dict.keys())
    return label, data


def get_daily_sales(*args, **kwargs):
    # Returns a dictionary containing the daily sales
    logger.info('Function Name: get_daily_sales')
    start_time = perf_counter()
    date = get_present_date().date()
    d_sales = 0
    logger.debug(f'Day: {date}')

    try:
        obj = DailySale.objects.get(date=date)
        d_sales = obj.total_sales
    except Exception as e:
        logger.error(f"get_daily_sales: {e}")

    if settings.DEBUG:
        logger.info(f"Execution Time: {perf_counter() - start_time}")

    return d_sales


def get_weekly_sales(*args, **kwargs):
    logger.info('Function Name: get_weekly_sales')
    start_time = perf_counter()
    total_sales = 0

    week_range = get_week_date_range(get_present_date().date())
    week_sales = DailySale.objects.filter(
        Q(date__range=(week_range[0], week_range[1])))

    for sales in week_sales:
        total_sales += sales.total_sales

    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    return total_sales


def get_monthly_sales(*args, **kwargs):
    logger.info('Function Name: get_monthly_sales')
    start_time = perf_counter()
    # DD always = 1 to make yyyy/mm format
    special_date = month_year(get_present_date().date())
    m_sale = 0
    try:
        obj = MonthlySale.objects.get(month_year=special_date)
        m_sale = obj.total_sales
    except Exception as e:
        logger.error(f"get_monthly_sale: {e}")
    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time}')

    return m_sale


def get_yearly_sales(*args, **kwargs):
    logger.info('Function Name: get_yearly_sales')
    start_time = perf_counter()
    year = get_present_year()
    total_sales = 0

    try:
        x = YearlySale.objects.get(year=year)
        total_sales = x.total_sales
    except Exception as e:
        logger.error(f'get_yearly_sales(): {e}')

    if settings.DEBUG:
        logger.info(f'Execution Time: {perf_counter() - start_time  }')

    return total_sales
