import logging
import re
from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .context_processors import new_order_id
# from django.http import JsonResponse
from .models import Item, Order, OrderItem
from .receipt_backend import ReceiptPrinter
from .utils import (
    check_order_status,
    delete_order_item,
    get_order_or_none
)

#  logging setup
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


def index(request):
    logger.info('Function Name: index')
    order_id = None
    try:
        order_id = int(request.GET['orderid'])
        logger.debug(f'UpdateOrder: {order_id}')
        order = Order.objects.get(pk=order_id)
        if not order.is_paid:
            order.is_update = True
            order.save()
            logger.debug(f'IsUpdate: {order.is_update}')
            context = {'order': order}
            return render(request, 'index.html', context)

        else:
            return render(request, 'modal.html', {'order': order,
                                                  'error': "Cannot update a paid order"})
    except KeyError:
        order_id = new_order_id(request).get('new_order_id')
        logger.debug(f'Received Order: {order_id}')
        order = Order.objects.get_or_create(pk=order_id)
        context = {'order': order[0], }
        return render(request, 'index.html', context)


@csrf_exempt
def search_items(request):
    logger.debug('Function Name: search_items')
    item_name = request.GET.get('item-name')
    order_id = request.GET.get('orderid')
    order = Order.objects.get(pk=order_id)
    suggestions: list = []
    print("Indes____________-")
    try:
        index_number = int(item_name)
        suggestions = Item.objects.filter(pk=index_number)

    except ValueError:
        suggestions = Item.objects.filter(name__icontains=item_name)
        # print(suggestions)

    return render(request, 'partials/search-results.html',
                  context={
                      "suggestions": suggestions,
                      "order": order,
                  },
                  )


@csrf_exempt
def add_item(request, item_id):
    logger.debug('Function Name: add_item')
    #  adds item to the order
    order_id = request.GET['orderid']
    logger.debug(f"Received order_id: {order_id}")
    item = Item.objects.get(pk=item_id)
    order = Order.objects.get_or_create(pk=order_id)[0]
    if item in order.items.all():
        logger.debug(f'Item {item.name} already in order {order_id}')
        order_item = order.orderitem_set.get(item__pk=item_id)
        order_item.quantity += 1
        order_item.save()
        logger.info(
            f'Updated order_item {order_item.item.name} for order {order_item.order.id}')
        context = {"order": order,
                   'message': f'Item already in order. Updated Quantity to {order_item.quantity}'}
        return render(
            request,
            'partials/show-added-items.html',
            context
        )
    logger.debug(f'Received item {item.name}')
    order_item = OrderItem.objects.create(
        order=order,
        item=item)
    order_item.save()
    logger.info(
        f'Created order_item {order_item.item.name} for order {order_item.order.id}')
    context = {"order": order}
    return render(
        request,
        'partials/show-added-items.html',
        context
    )


@csrf_exempt
def update_item_quantity(request, item_id, order_id):
    logger.debug('Function Name: update_item_quantity')
    # updates the quantity of the item in the order
    quantity = request.POST.get('item-quantity')
    order = Order.objects.get(pk=order_id)
    logger.debug(f'Got order: {order}')
    order_item = order.orderitem_set.get(item__pk=item_id)
    logger.debug(f'Got relative order_item: {str(order_item.item)}')
    order_item.quantity = quantity
    logger.debug(f'Updated quantity: {order_item.quantity}')
    order_item.save()
    context = {"order": order}
    return render(request, 'partials/show-added-items.html', context)


@csrf_exempt
def delete_item(request, order_id, item_id):
    logger.info('Function Name: delete_item')
    order = delete_order_item(order_id, item_id)
    context = {
        'order': order
    }
    return render(request,
                  'partials/show-added-items.html', context)


@csrf_exempt
def delete_order(request, order_id):
    logger.info('Function Name: delete_order')
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect('billing:index')


@csrf_exempt
def create_order(request):
    order_id = int(request.GET['order_id'])
    logger.debug('Function Name: create_order')
    logger.debug(f'Received Order {order_id}')
    order = Order.objects.get(pk=order_id)
    if order.has_items():
        order.is_new = False
        order.total_price = order.get_total_price()
        order.save()
        logger.info(f'Saved order {order_id}')
        new_order = Order.objects.create(pk=order_id+1)
        logger.debug(f'Created new order {order_id+1}')
        context = {
            'prev_order': order,
            'order': new_order,
        }
        return render(request, 'index.html', context)

    context = {
        'order': order,
        'message': "Order is empty. Please add items to the order."
    }
    return render(request, 'index.html', context)


@csrf_exempt
def update_order(request, order_id):
    logger.info('Function name: update_order')
    logger.info(f'OrderId: {order_id}')
    order = Order.objects.get(pk=order_id)
    logger.debug(f'Got order {order.id}')
    order.is_udpate = False
    order.total_price = order.get_total_price()
    order.save()
    next_order_id = new_order_id(request).get('new_order_id')
    next_order = Order.objects.get(pk=next_order_id)
    logger.debug(f'Got next order {next_order.id}')
    context = {
        'order': next_order}
    return render(request, 'index.html', context)


@csrf_exempt
def update_table_number(request, order_id):
    logger.debug('Function Name: update_table_number')
    logger.info(f'Updating table number for order {order_id}')
    order = Order.objects.get(pk=order_id)
    logger.debug(f'Got order {order.id}')
    table_number = request.POST.get('table-number')
    logger.debug(f'Got table number {table_number}')
    old_table_number = order.table_number
    order.table_number = table_number
    order.save()
    logger.info(
        f'Updated table number for order {order.id} from {old_table_number} to {order.table_number}'
    )
    logger.debug(
        f'Updated table number in Order {order.id} is {order.table_number}')

    context = {
        'order': order,
    }
    return render(request, 'index.html', context)


@csrf_exempt
def modal_view(request, order_id):
    logger.debug('Function: modal_view')
    order = Order.objects.get(pk=order_id)
    logger.debug(f'Got order: {order.id} Reqeuested Order: {order_id}')
    json_data = serializers.serialize('json', [order,])
    context = {
        'order': order,
        'order_id': order.id,
        'json_order': json_data
    }
    return render(request, 'modal.html', context)


@csrf_exempt
def modal_save(request):
    logger.info('Function Name: modal_save')
    order_id = request.GET.get('orderid')
    logger.debug(f'Received OrderId from GET: {order_id}')
    order = Order.objects.get(pk=order_id)
    order.is_paid = True
    order.order_status = "Paid"
    order.save()
    logger.info(f'Order.is_paid: {order.is_paid}')
    logger.info(f'Order {order.id} is paid')
    order_id = new_order_id(request).get('new_order_id')
    logger.debug(f'Received Order: {order_id}')
    order = Order.objects.get_or_create(pk=order_id)
    context = {'order': order[0], }
    return render(request, 'index.html', context)


@csrf_exempt
def print_receipt_view(request, order_id):
    logger.debug('Function: print_receipt_view')
    logger.info(f'OrderId: {order_id}')
    order = Order.objects.get(pk=order_id)
    logger.debug('Function: print_receipt_view')

    printer = ReceiptPrinter(order)
    printer.print_receipt()
    context = {
        'order': order,
    }
    return render(request, 'modal.html', context)


@csrf_exempt
def search_orders(request):
    logger.info('Function Name: search_orders')
    order_id = request.POST.get('order-id')
    if order_id:
        logger.debug(f'Received order_id: {order_id}')
        order = get_order_or_none(order_id)
        if order and not order.is_new:
            logger.debug('Order found')
            context = {
                'orders': [order],
                'json_order_data': serializers.serialize('json', [order,]),
            }
            return render(request, 'partials/order-search-results.html', context)
        else:
            logger.warn('Order Not Found')
            context = {
                'message': 'No orders found',
            }
            return render(request, 'partials/order-search-results.html', context)
    else:
        context = {
            'message': 'No orders found',
        }
        return render(request,
                      'partials/order-search-results.html',
                      context)


@csrf_exempt
def update_order_status(request, order_id):
    logger.info('Function Name: update_order_status')
    order = Order.objects.get(pk=order_id)
    logger.debug(f'Fetched order: {order.id} Requested order: {order_id}')
    order_status = request.POST.get('order-status')

    # check order status is equal to order_status
    if check_order_status(order.order_status, order_status):
        logger.warning(
            f'Order_status is already set to {order_status}')
        orders = Order.objects.filter(
            Q(is_paid=False) & Q(is_new=False)).order_by('-id')
        context = {
            'orders': orders,
            'order': order,
        }
        return render(request,
                      'partials/order-search-results.html',
                      context)
    logger.debug(f'Received order status: {order_status}')
    if order_status == 'Paid':
        # if order status is paid
        # we change the is_paid status to true
        # so that the order will not be shown in recent orders
        order.order_status = order_status
        order.is_paid = True
        order.save()
        logger.info(f'Updated order {order.id} status to {order_status}')
        orders = Order.objects.filter(
            Q(is_paid=False) & Q(is_new=False)).order_by('-id')
        context = {
            'orders': orders,
            'order': order,
            'status': order_status,
        }
        return render(request, 'partials/order-search-results.html', context)

    # if order status is delivered
    # we don't change the is_paid status to true
    # so that the order will still be in shown in recent orders
    order.order_status = order_status
    order.save()
    logger.info(f'Updated order {order.id} status to {order_status}')
    orders = Order.objects.filter(
        Q(is_paid=False) & Q(is_new=False)).order_by('-id')
    context = {
        'orders': orders,
        'order': order,
        'status': order_status,
    }
    return render(request, 'partials/order-search-results.html', context)


@csrf_exempt
def update_payment_method(request, order_id):
    logger.info('Function Name: update_payment_method')
    order = Order.objects.get(pk=order_id)
    logger.debug(f'Fetched order: {order.id} Requested order: {order_id}')
    payment_method = request.POST.get('payment-method')
    logger.debug(f'Received payment method: {payment_method}')
    order.payment_method = payment_method
    order.save()
    logger.info(f'Updated order {order.id} payment method to {payment_method}')
    json_data = serializers.serialize('json', [order,])
    logger.debug(json_data)
    context = {
        'order': order,
        'json_order': json_data,
    }
    return render(request, 'modal.html', context)
