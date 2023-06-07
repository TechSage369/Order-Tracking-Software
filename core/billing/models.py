import re
import datetime
from typing import Iterable, Optional
from django.db import models


class Order(models.Model):
    ORDER_STATUS_CHOICE = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    ]
    ordered_on = models.DateTimeField(auto_now_add=True)
    paid_online = models.BooleanField(default=False)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICE,
                                    max_length=10,
                                    default=ORDER_STATUS_CHOICE[0][0])
    #  is_new returns True if the order is recently created
    #  and has no items in it
    #  but if set to False
    #  all the items are set and it is finally saved as a model.
    is_new = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    is_update = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, default='Cash')
    items = models.ManyToManyField('Item', through="OrderItem")
    table_number = models.PositiveIntegerField(default=1)
    total_price = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_price = sum([order_item.get_price() for order_item in self.orderitem_set.all()]
        super().save(*args, **kwargs)

    def get_id(self):
        """
        Returns the id of the order
        """
        return self.pk

    def get_total_price(self):
        """
        Returns the total price of the order.
        This includes the sum of the toal prices of the items that 
        are ordered.
        """
        return sum([order_item.get_price() for order_item in self.orderitem_set.all()])

    def get_payment_mode(self):
        '''
        returns the payment mode of the order.
        if paid_online is True, it returns 'Online'
        else it returns 'Cash'
        '''
        return 'Online' if self.paid_online else 'Cash'

    def get_order_date(self):
        """
        Returns the date of the order.
        """
        return self.ordered_on.strftime('%b %d, %Y')

    def has_items(self):
        """
        Returns True when there are items
        Returns False when no items are there
        """
        return False if len(self.items.all()) <= 0 else True

    def __str__(self):
        return f"OrderId: {self.pk} Table: {self.table_number} Total: {self.total_price}"


class Item(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    price = models.IntegerField(default=0)

    def get_quantity(self):
        return self.orderitem_set.all()[0].quantity

    def get_total_price(self):
        return self.get_quantity() * self.price

    def get_shortened_name(self):
        if 'chicken' in self.name.lower():
            new_name = re.sub('chicken', 'chk', self.name.lower()).upper()
            if len(new_name) > 11:
                return new_name[:11].upper()
            if len(new_name) < 11:
                new_name += " "*(11-len(new_name))
                return new_name.upper()
        if 'pork' in self.name.lower():
            new_name = re.sub('pork', 'prk', self.name.lower()).upper()
            if len(new_name) > 11:
                return new_name[:11].upper()
            if len(new_name) < 11:
                new_name += " "*(11-len(new_name))
                return new_name.upper()
        if len(self.name) < 11:
            return self.name.upper() + " "*(11-len(self.name))
        return self.name[:11].upper()

    def get_price(self):
        return f"{self.price}"

    def __str__(self):
        return f"{self.id}. {self.name} - Rs. {self.price}"


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.item.name} - {self.quantity} - Rs. {self.item.price}"
