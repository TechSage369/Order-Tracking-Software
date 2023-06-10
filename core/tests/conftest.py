import pytest
import random
from typing import List
from datetime import datetime
from .utils import get_custom_date
from billing.models import Order, Item, OrderItem
from custom_types import OrderType


@pytest.fixture
def order_data():
    id_ = 0
    order = Order.objects.create(pk=id_)
    return order


@pytest.fixture
def item_data():
    item = Item.objects.create(pk=0,
                               name="Mock Tea",
                               price="100")
    return item


@pytest.fixture
def order_item_data(order_data, multilple_items):
    print(order_data)

    for items in multilple_items:
        order_data.items.add(items)
    return order_data


@pytest.fixture
def orderitem_data(order_data, item_data):
    orderitem = OrderItem.objects.create(order=order_data,
                                         item=item_data,
                                         quantity=3)
    return orderitem


@pytest.fixture
def item_name():
    name = "Chicken Fried Rice"
    id_ = 0
    price = 10
    return Item.objects.create(id=id_,
                               name=name,
                               price=price)


@pytest.fixture
def multilple_items():
    items = []
    seed = random.randint(1, 7)
    for i in range(seed):
        item = Item.objects.create(id=i,
                                   name=f'Item{i}',
                                   price=10)
        items.append(item)
    return items


@pytest.fixture
def create_order_factory(item_name) -> List[OrderType]:

    def _create_order(pk: int, ordered_on: datetime):
        order = Order.objects.create(
            pk=pk,
            ordered_on=ordered_on
        )
        order.items.add(item_name)
        order.is_new = False
        order.is_paid = True
        order.save()
        return order

    return _create_order


@pytest.fixture
def multiple_orders(create_order_factory):
    order_limit = 21
    month = 1
    orders = []

    for i in range(1, 21):
        date = get_custom_date(
            month=month,
            day=i,
        )

        orders.append(create_order_factory(
            pk=i,
            ordered_on=date,
        ))

    return month, orders
