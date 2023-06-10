from django import forms

from billing.models import Item


class CreateNewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']
