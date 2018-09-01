from django import forms
import datetime

from .models import Zakup

class ZakupForm(forms.ModelForm):

    class Meta:
        model = Zakup
        fields = ('category', 'month', 'year', 'name', 'price', 'quantity',)
