import calendar
import datetime

from .models import Item, Order, OrderItem


def delete_order_item(order_id, item_id):
    # deletes order item from order
    print(f"Deleting Item: {item_id} in Order: {order_id}")
    order = Order.objects.get(pk=order_id)
    print(f"Order: {order}")
    order_item = Item.objects.get(pk=item_id)
    print(f"OrderItem: {str(order_item)}")
    order.items.remove(order_item)
    return order


def get_order_or_none(order_id):
    # returns order object or None
    try:
        order = Order.objects.get(pk=order_id)
        return order
    except Order.DoesNotExist:
        return None


def get_current_date():
    #  returns formatted date string
    date_object = datetime.date.today()
    year, month, day = date_object.year, calendar.month_name[date_object.month], date_object.day
    return f"{month} {day}, {year}"


def check_order_status(order_status, received_status):
    #  checks if order status is the same as received status
    return order_status == received_status
