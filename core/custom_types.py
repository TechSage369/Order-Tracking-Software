from typing import Type
from django.db.models import Model


class OrderType(Type[Model]):
    pass


class ItemType(Type[Model]):
    pass


class OrderItemType(Type[Model]):
    pass
