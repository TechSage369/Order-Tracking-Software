"""
Printer Configuration File
A and B represent the hex code of the printer
INTERFACE is the interface of the printer
EP_IN and EP_OUT are the endpoints of the printer
"""
import os

from django.conf import settings

print(settings.BASE_DIR)

A = 0x0456
B = 0x0808
INTERFACE = 4
EP_IN = 0x81
EP_OUT = 0x03
LOGO = settings.BASE_DIR / "billing/static/img/logo_index.jpeg"
