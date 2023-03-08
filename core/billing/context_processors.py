from .models import Order
from datetime import datetime
import logging
from django.conf import settings


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
            'class': 'logging.FileHandler',
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
    logger.debug(
        f"Total orders: {len(orders)} from {orders[0].id} to {orders[len(orders) - 1].id}")
    new_order_id = 1
    if orders:
        logger.info("There are orders in the database")
        last_order = orders[len(orders) - 1]
        logger.info(f"Got last order: {str(last_order)}")
        if last_order.is_new:
            logger.info(f"new_order_id: {last_order.id}")
            return {
                "new_order_id": last_order.id,
                "new_order_date": last_order.ordered_on,
            }
        else:
            new_order_id = last_order.id + 1
            logger.info(f"New order id: {new_order_id}")
    new_order_date = datetime.now()
    return {
        'new_order_id': new_order_id,
        'new_order_date': new_order_date,
    }


def all_orders(request):
    logger.debug("Function Name: all_orders")
    #  Returns all orders
    orders = Order.objects.filter(is_new=False).order_by('-ordered_on')
    logger.debug(
        f'Orders contains {len(orders)} orders from {orders[0].id} to {orders[len(orders) - 1].id}')
    total_orders = len(orders)
    context = {
        'orders': orders[0:total_orders-1],
        'length': total_orders,
    }
    return context
