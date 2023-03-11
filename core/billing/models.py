from django.db import models
from uuid import uuid4 as uuid
import re

# Create your models here.


class Order(models.Model):
    ORDER_STATUS_CHOICE = [
        ('Waiting', 'Waiting'),
        ('Delivered', 'Delivered'),
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
    items = models.ManyToManyField('Item', through="OrderItem")
    table_number = models.PositiveIntegerField(default=1)

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

    def __str__(self):
        return f"OrderId: {self.pk} Table: {self.table_number}"


class Item(models.Model):
    name = models.CharField(max_length=120)
    price = models.IntegerField(default=0)

    def get_quantity(self):
        return self.orderitem_set.all()[0].quantity

    def get_shortened_name(self):
        if 'chicken' in self.name.lower():
            new_name = re.sub('chicken', 'chk', self.name.lower()).upper()
            if len(new_name) > 11:
                return new_name[:11]
        if 'pork' in self.name.lower():
            new_name = re.sub('pork', 'prk', self.name.lower()).upper()
            if len(new_name) > 11:
                return new_name[:11]
        return self.name[:11].upper()

    def get_price(self):
        return f"Rs.{self.price}"

    def get_total_price(self):
        return f"Rs. {self.get_quantity() * self.price}"

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
