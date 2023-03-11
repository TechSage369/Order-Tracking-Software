from .models import Order, Item, OrderItem


def delete_order_item(order_id, item_id):
    print(f"Deleting Item: {item_id} in Order: {order_id}")
    order = Order.objects.get(pk=order_id)
    print(f"Order: {order}")
    order_item = Item.objects.get(pk=item_id)
    print(f"OrderItem: {str(order_item)}")
    order.items.remove(order_item)
    return order
