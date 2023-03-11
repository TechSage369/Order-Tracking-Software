from django import forms
from django.forms import formset_factory
from .models import Item, Order


class AddItem(forms.Form):
    item_name = forms.ModelChoiceField(queryset=Item.objects.all())


class UpdateItem(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']
