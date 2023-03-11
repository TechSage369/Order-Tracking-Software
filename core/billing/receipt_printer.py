from escpos.printer import Usb
import logging
from .conf import A, B, INTERFACE, EP_IN, EP_OUT, LOGO
from PIL import Image
from .models import Order
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


def get_logo():
    logger.info('Function: get_logo')
    # Get logo here
    logo = Image.open(LOGO)
    logo = logo.resize((logo.width // 2, logo.height // 2)).convert("1")
    return logo


def print_receipt(order=None):
    order = Order.objects.get(pk=4)
    p = Usb(A, B, INTERFACE, EP_IN, EP_OUT)
    logger.debug('Function: print_receipt')
    logger.debug('Printing receipt')
    p.image(get_logo())
    p.text(f"{'-'*32}\n")
    p.text("HomeTown Pizzeria and Restaurant\n")
    p.text("Singhmari, Darjeeling\n")
    p.text('Ph no: 1234567890\n')
    p.text(f'orderID: 1234567890\n')
    p.text(f'TableNo: {order.table_number}\n')
    p.text(f"{'-'*32}\n")
    p.text('{:8} {:>5} {:>5} {:>8}\n'.format('Item', 'Qty', 'Rate', 'Price'))
    for item in order.items.all():
        if len(item.get_shortened_name()) < 10:
            p.text('{:10} {:>3} {:>5} {:>8}\n'.format(
                item.get_shortened_name(), item.get_quantity(), item.get_price(), item.get_total_price()))
        else:
            p.text('{:4} {:>2} {:>5} {:>8}\n'.format(
                item.get_shortened_name(), item.get_quantity(), item.get_price(), item.get_total_price()))
    p.text(f"{'-'*32}\n")
    p.text(f"Total Price: Rs.{order.get_total_price()}\n")
    p.text('Thank you for coming!\n')
    p.text('Visit Again!\n')
    p.close()
