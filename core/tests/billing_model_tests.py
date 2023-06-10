import pytest
import random
import datetime
import calendar
from billing.models import Item, Order
from billing.utils import (delete_order_item,
                           get_order_or_none,
                           check_order_status,
                           get_current_date)


@pytest.mark.django_db
class TestOrderModel:
    def test_order_status_is_waiting(self):
        # Create object in mock database
        obj1 = Order.objects.create()
        assert obj1.order_status == 'Unpaid'

    def test_order_status_is_delivered(self):
        obj1 = Order.objects.create(order_status='Delivered')
        assert obj1.order_status == 'Delivered'

    def test_order_status_is_paid(self):
        obj1 = Order.objects.create(order_status='Paid')
        assert obj1.order_status == 'Paid'

    def test_order_paid_online_is_true(self):
        obj1 = Order.objects.create(paid_online=True)
        assert obj1.paid_online == True

    def test_order_paid_online_is_false(self):
        obj1 = Order.objects.create(paid_online=False)
        assert obj1.paid_online == False

    def test_order_get_id(self):
        obj1 = Order.objects.create()
        assert obj1.get_id() == obj1.pk

    def test_order_get_total_price(self, order_item_data):
        total_price = 10 * len(order_item_data.items.all())
        assert order_item_data.get_total_price() == total_price

    def test_order_get_order_payment_mode_online(self, order_item_data):
        order_item_data.paid_online = True
        assert "Online" == order_item_data.get_payment_mode()

    def test_order_get_order_payment_mode_cash(self, order_item_data):
        order_item_data.paid_online = False
        assert "Cash" == order_item_data.get_payment_mode()

    def test_order_has_items_false(self, order_data):
        assert False == order_data.has_items()

    def test_order_has_items_true(self, order_item_data):
        assert True == order_item_data.has_items()


@pytest.mark.django_db
class TestItemOrder:
    def test_item_name(self):
        orderObj = Order.objects.create()
        obj1 = Item.objects.create(name='Test')
        assert obj1.name == 'Test'

    def test_item_price(self):
        orderObj = Order.objects.create()
        obj1 = Item.objects.create(name='Test', price=100)
        assert obj1.price == 100

    def test_item_get_quantity(self, orderitem_data):
        item = orderitem_data.item
        assert item.get_quantity() == orderitem_data.quantity

    def test_item_get_shortened_name_chk(self, item_name):
        res = "chk fried r".upper()
        assert item_name.get_shortened_name() == res

    def test_item_get_shortened_name_chk_short(self, item_name):
        item_name.name = "Chicken tea"
        item_name.save()
        res = "chk tea    ".upper()
        assert res == item_name.get_shortened_name()

    def test_item_get_shortened_name_pork(self, item_name):
        item_name.name = "Pork Fried Rice"
        item_name.save()
        res = "prk fried r".upper()
        assert res == item_name.get_shortened_name()

    def test_item_get_shortened_name_pork_short(self, item_name):
        item_name.name = "Pork Tea"
        item_name.save()
        res = "prk tea    ".upper()
        assert res == item_name.get_shortened_name()

    def test_item_get_shortened_len(self, item_name):
        item_name.name = "Tea"
        item_name.save()
        res = "tea        ".upper()
        assert res == item_name.get_shortened_name()

    def test_item_get_shortened_equal_len(self, item_name):
        item_name.name = "Ababab Momo"
        item_name.save()
        res = "ababab momo".upper()
        assert res == item_name.get_shortened_name()

    def test_item_get_price(self, item_name):
        assert item_name.get_price() == str(item_name.price)

    def test_item_get_price_hard_code(self, item_name):
        assert item_name.get_price() == "10"


@pytest.mark.django_db
class TestUtils:
    def test_get_order_or_none_true(self):
        order_id = 1
        new_order = Order.objects.create(pk=order_id)
        order = get_order_or_none(order_id)
        assert order.id == 1

    def test_get_order_or_none_false(self):
        order_id = 0
        order = get_order_or_none(order_id)
        assert order == None

    def test_delete_order_item(self, order_item_data):
        items = order_item_data.items.all()
        item_to_delete = random.choice(items)
        order_after_delete = delete_order_item(order_id=order_item_data.id,
                                               item_id=item_to_delete.id)
        assert item_to_delete.id not in [
            item.id for item in order_after_delete.items.all()]

    def test_check_order_status_pass(self, order_data):
        order_data.status = "Paid"
        order_status = "Paid"
        result = check_order_status(order_status=order_status,
                                    received_status=order_data.status)
        assert True == result

    def test_check_order_status_fail(self, order_data):
        order_data.status = "Unpaid"
        order_status = "Paid"
        result = check_order_status(order_status=order_status,
                                    received_status=order_data.status)
        assert False == result

    def test_get_current_date(self):
        date = datetime.date.today()
        year, month, day = date.year, calendar.month_name[date.month], date.day
        res = f"{month} {day}, {year}"
        assert res == get_current_date()
