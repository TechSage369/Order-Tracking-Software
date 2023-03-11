import pytest
from .models import Order, Item


@pytest.mark.django_db
class TestModels:
    def test_order_status_is_waiting(self):
        # Create object in mock database
        obj1 = Order.objects.create()
        assert obj1.order_status == 'Waiting'

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

    def test_item_name(self):
        orderObj = Order.objects.create()
        obj1 = Item.objects.create(name='Test')
        assert obj1.name == 'Test'

    def test_item_price(self):
        orderObj = Order.objects.create()
        obj1 = Item.objects.create(name='Test', price=100)
        assert obj1.price == 100
