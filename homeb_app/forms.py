from django import forms

from .models import Zakup

class ZakupForm(forms.ModelForm):

    class Meta:
        model = Zakup
        fields = ('category', 'month', 'name', 'price', 'quantity',)
