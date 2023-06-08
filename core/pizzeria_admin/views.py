import logging
import random
import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from billing.context_processors import new_order_id
from billing.models import Item, Order, OrderItem

from .forms import CreateNewItemForm
from .utils import (
    generate_labels_for_month,
    get_present_month,
    make_new_year_range)
from .sales_data import (
    get_daily_data,
    get_weekly_data,
    get_monthly_data,
    get_yearly_data,
    get_daily_sales,
    get_weekly_sales,
    get_monthly_sales,
    get_yearly_sales,
)

# All admin related views here

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


@csrf_exempt
def pizzeria_login(request):
    logger.debug('Function Name: pizzeria_login')
    form = AuthenticationForm
    if request.method == 'POST':
        logger.info('Received POST request')
        form = AuthenticationForm(data=request.POST)
        logger.info('Received form data')
    if request.method == 'POST':
        logger.info('Received POST request')
        form = AuthenticationForm(data=request.POST)
        logger.info('Received form data')
        if form.is_valid():
            logger.info('Form is valid')
            logger.info('Form is valid')
            user = form.get_user()
            logger.info('Got user')
            logger.info('Got user')
            if user is not None:
                logger.info('User exists!')
                logger.info('User exists!')
                login(request, user)
                return redirect('pizzeria_admin:admin')
            else:
                logger.info('User does not exist')
                context = {
                    'login_form': form,
                    'error_message': 'User does not exist!',
                }
                return render(request, 'pizzeria_admin/pizzeria-login.html', context)
        else:
            context = {
                'login_form': form,
                'error_message': 'Invalid Credentials',
            }
            return render(request, 'pizzeria_admin/pizzeria-login.html', context)
    if request.method == "GET":
        logger.info('Received GET request')
        context = {
            'login_form': form,
            'error_message': 'Invalid Credentials',
        }
        return render(request, 'pizzeria_admin/pizzeria-login.html', context)
    if request.method == "GET":
        logger.info('Received GET request')
        context = {
            'login_form': form,
            'login_form': form,
        }
        return render(request, 'pizzeria_admin/pizzeria-login.html', context)


@csrf_exempt
@login_required
def pizzeria_logout(request):
    logout(request)
    return redirect('billing:index')


@login_required
@csrf_exempt
def pizzeria_admin(request):
    logger.debug('Function Name: pizzeria_admin')
    logger.debug(f'Method: {request.method}')
    form = CreateNewItemForm
    if request.method == "POST":
        form = CreateNewItemForm(request.POST)
        if form.is_valid():
            logger.info(f'Validation: {form.is_valid()}')
            new_item = form.save()
            logger.debug(f'Created new item: {new_item.name}')
            items = Item.objects.all().order_by('-pk')
            form = CreateNewItemForm
            context = {
                'items': items,
                'form': form,
                'message': f'New Item Added: {new_item.name}'
            }
            return render(request, 'pizzeria_admin/partials/show-all-items.html', context)
        else:
            logger.error('Received Form is Invalid')
            items = Item.objects.all().order_by('-pk')
            form = CreateNewItemForm
            context = {
                'items': items,
                'form': form,
                'message': "Invalid Form"
            }
    items = Item.objects.all().order_by('-pk')
    logger.debug(f'Collected all items {items}.')
    context = {
        'items': items,
        'form': form,
    }
    return render(request, 'pizzeria_admin/pizzeria-admin.html', context)


@login_required
def admin_logout(request):
    order_id = new_order_id(request).get('new_order_id')
    user = request.user
    logout(request)
    order = Order.objects.get_or_create(pk=order_id)
    context = {'order': order}
    return redirect('billing:index')


@login_required
def statistics(request):
    logger.info('Function Name: statistics')
    daily_label, daily_data = get_daily_data()
    weekly_label, weekly_data = get_weekly_data()
    monthly_label, monthly_data = get_monthly_data()
    yearly_label, yearly_data = get_yearly_data()
    context = {
        'daily_label': daily_label,
        'daily_data': daily_data,
        'weekly_label': weekly_label,
        'weekly_data': weekly_data,
        'monthly_label': monthly_label,
        'monthly_data': monthly_data,
        'yearly_label': yearly_label,
        'yearly_data': yearly_data,
        'daily_sales': get_daily_sales(),
        'weekly_sales': get_weekly_sales(),
        'monthly_sales': get_monthly_sales(),
        'yearly_sales': get_yearly_sales(),
    }
    return render(
        request,
        'pizzeria_admin/statistics.html',
        context,
    )


@ csrf_exempt
@ login_required
def delete_item_from_model(request, item_id):
    logger.info('Function Name: delete_item_from_model')
    form = CreateNewItemForm
    item = Item.objects.get(pk=item_id)
    name = item.name
    #  delete item
    item.delete()
    items = Item.objects.all().order_by('-pk')
    context = {
        'message': f'Item {name} Deleted!',
        'form': form,
        'items': items,
    }
    return render(request, 'pizzeria_admin/pizzeria-admin.html', context)


@login_required
def order_history(request):
    orders = Order.objects.all().filter(Q(is_paid=True) & Q(is_new=False))
    context = {
        'orders': orders
    }
    return render(request, 'pizzeria_admin/order-history.html', context)


@login_required
def order_detail_view(request, order_id):
    order = Order.objects.get(pk=order_id)
    context = {
        'order': order
    }
    return render(request, 'pizzeria_admin/partials/order-detail.html', context)


@login_required
def order_history_search(request):
    logger.info('Function Name: order_history_search')
    order_id = request.GET.get('order-query')
    logger.debug(f'Order ID: {order_id}')
    order = Order.objects.get(pk=order_id)
    context = {
        'orders': [order],
    }
    return render(request, 'pizzeria_admin/partials/show-all-orders.html', context)


@csrf_exempt
@login_required
def search_items(request):
    logger.info('Function Name: search_items')
    item_name = request.POST.get('item-query')
    logger.debug(f'Item Name: {item_name}')
    items = Item.objects.filter(name__icontains=item_name)
    context = {
        'items': items,
    }
    return render(request, 'pizzeria_admin/partials/show-all-items.html', context)


@login_required
def item_update(request, id):
    instance = get_object_or_404(Item, pk=id)
    form = CreateNewItemForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('pizzeria_admin:admin')
    return render(request, "pizzeria_admin/item-update.html", {'form': form})
