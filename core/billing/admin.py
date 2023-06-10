from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Item, Order, OrderItem


class OrderAdminModel(admin.ModelAdmin):
    # Add the fields you want to make read-only from the admin dashboard
    readonly_fields = ('total_price', 'is_paid')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            return self.readonly_fields  # Return the fields as read-only
        return ()  # Otherwise, return an empty tuple to allow modifications

    def has_delete_permission(self, request, obj=None):
        return False  # Return False to disable the delete permission


admin.site.register(Order, OrderAdminModel)
admin.site.register(Item)

admin.site.unregister(User)
admin.site.unregister(Group)
