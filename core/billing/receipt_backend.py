import platform
from escpos.printer import Usb
from .conf import EP_IN, EP_OUT, INTERFACE, LOGO, A, B
from .receipt_printer import print_receipt_linux, print_receipt_windows
import logging
from django.conf import settings

SYSTEM = platform.platform()

if 'windows' in SYSTEM.lower():
    from win32printing import Printer

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


class ReceiptPrinter:
    '''
    ReceiptPrinter class to print receipt.
    Arguments are:
    order: the Order object
    title_font (default 10): used to manage title font for windows backend
    font (default 8): used to manage font size for windows backend
    weight (default 10): same as font
    '''

    def __init__(self, order, title_font=10, font=8, weight=10):
        self.order = order
        self.title_font = title_font
        self.font = font
        self.weight = weight
        self.os = None

    def get_printer_backend(self):
        if 'windows' in SYSTEM.lower():
            logger.info('Found system to be Windows using windows backend.')
            self.os = 'windows'
            logger.debug(f'Set self.os to {self.os}')
            return Printer(linegap=1)

        if 'linux' in SYSTEM.lower():
            logger.info('Found system to be linux using linux backend.')
            self.os = 'linux'
            logger.debug(f'Set self.os to {self.os}')
            return Usb(A, B, INTERFACE, EP_IN, EP_OUT)

    def print_receipt(self):
        printer = self.get_printer_backend()
        logger.debug(printer)
        if self.os == 'windows':
            print_receipt_windows(self.order, printer,
                                  self.font, self.title_font, self.weight)
        if self.os == 'linux':
            print_receipt_linux(self.order, printer)
