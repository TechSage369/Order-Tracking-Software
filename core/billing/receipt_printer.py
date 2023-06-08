import logging

from django.conf import settings
from escpos.printer import Usb
from PIL import Image

from .conf import EP_IN, EP_OUT, INTERFACE, LOGO, A, B
from .models import Order

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


def get_logo():
    logger.info('Function: get_logo')
    # Get logo here
    logo = Image.open(LOGO)
    logo = logo.resize((logo.width // 2, logo.height // 2)).convert("1")
    return logo


def print_receipt_linux(order, printer):
    p = Usb(A, B, INTERFACE, EP_IN, EP_OUT)
    logger.debug('Function: printerrint_receipt_linux')
    logger.debug('Printing receipt')
    printer.image(get_logo())
    printer.text(f"{'-'*32}\n")
    printer.text("HomeTown Pizzeria and Restaurant\n")
    printer.text("Singhmari, Darjeeling\n")
    printer.text('Ph no: 7001497783\n')
    printer.text(f'orderID: {order.id}\n')
    printer.text(f'TableNo: {order.table_number}\n')
    printer.text(f"{'-'*32}\n")
    printer.text('{:8} {:>5} {:>5} {:>8}\n'.format(
        'Item', 'Qty', 'Rate', 'Price'))
    for item in order.items.all():
        if len(item.get_shortened_name()) < 10:
            printer.text('{:10} {:>3} {:>5} {:>8}\n'.format(
                item.get_shortened_name(), item.get_quantity(), item.get_price(), item.get_total_price()))
        else:
            printer.text('{:4} {:>2} {:>5} {:>8}\n'.format(
                item.get_shortened_name(), item.get_quantity(), item.get_price(), item.get_total_price()))
    printer.text(f"{'-'*32}\n")
    printer.text(f"Total Price: Rs.{order.get_total_price()}\n")
    printer.text('Thank you for coming!\n')
    printer.text('Visit Again!\n')
    printer.close()


def print_receipt_windows(order, printer, fontsize, title_fontsize, weight):
    title_font = {'height': title_fontsize, 'weight': weight}
    font = {'height': fontsize}
    logger.info('Function: print_receipt_windows')
    logger.debug('Printing Receipt')
    with printer as printer:
        printer.text(f"{'-' * 32}\n", font_config=title_font)
        printer.text("HomeTown Pizzeria and Restaurant",
                     font_config=title_font)
        printer.text('Singamari, Darjeeling', font_config=title_font)
        printer.text('Ph No: 7001497783', font_config=title_font)
        printer.text(f"OrderId: {order.id}", font_config=title_font)
        printer.text(f"Date: {order.get_order_date()}", font_config=title_font)
        printer.text(
            f'TableNumber: {order.table_number}', font_config=title_font)
        printer.text(f"{'-' * 32}")
        printer.text('{:>11} {:>8} {:>5} {:>8}\n'.format(
            'Item', 'Qty', 'Rate', 'Price'), font_config=title_font)

        # printing items
        for item in order.orderitem_set.all():
            if len(item.item.get_shortened_name()) < 10:
                printer.text('{} {:>8} {:>5} {:>10}\n'.format(
                    item.item.get_shortened_name(),
                    item.quantity,
                    item.item.price,
                    item.get_price()
                ), font_config=font)
            else:
                printer.text('{} {:>8} {:>5} {:>10}\n'.format(
                    item.item.get_shortened_name(),
                    item.quantity, 
                    item.item.price, 
                    item.get_price()
                ), font_config=font)

        printer.text(f"{'-' * 32}\n", font_config=font)
        printer.text(
            f"Total Amount: Rs{order.get_total_price()}\n", font_config=title_font)
        printer.text('Visit Again!\n', font_config=title_font)
