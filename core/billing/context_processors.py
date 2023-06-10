import logging

from django.conf import settings
from django.db.models import Q

from .models import Order
from .utils import get_current_date

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


def new_order_id(request):
    logger.debug("Function Name: new_order_id")
    #  Returns new_order_id and new_order_date
    orders = Order.objects.all()
    new_order_id = 1
    if orders:
        logger.info("There are orders in the database")
        logger.debug(
            f"Total orders: {len(orders)} from {orders[0].id} to {orders[len(orders) - 1].id}")
        last_order = orders[len(orders) - 1]
        logger.info(f"Got last order: {str(last_order)}")
        if last_order.is_new:
            logger.info(f"new_order_id: {last_order.id}")
            return {
                "new_order_id": last_order.id,
                "new_order_date": get_current_date(),
            }
        else:
            new_order_id = last_order.id + 1
            logger.info(f"New order id: {new_order_id}")
    new_order_date = get_current_date()
    return {
        'new_order_id': new_order_id,
        'new_order_date': new_order_date,
    }


def all_orders(request):
    logger.debug("Function Name: all_orders")
    #  Returns all orders
    orders = Order.objects.filter(Q(is_paid=False) & Q(
        is_new=False)).order_by('-ordered_on')
    if orders:
        logger.debug(
            f'Orders contains {len(orders)} orders from {orders[0].id} to {orders[len(orders) - 1].id}')
    else:
        logger.debug("Orders is empty")
    total_orders = len(orders)
    context = {
        'orders': orders,
        'length': total_orders,
    }
    return context
