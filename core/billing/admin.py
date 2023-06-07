from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Item, Order, OrderItem

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderItem)

admin.site.unregister(User)
admin.site.unregister(Group)
