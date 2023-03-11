from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import (Order,
                     Item)


admin.site.register(Order)
admin.site.register(Item)

admin.site.unregister(User)
admin.site.unregister(Group)
