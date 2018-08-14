from django import forms

from .models import Zakup

class PostForm(forms.ModelForm):

    class Meta:
        model = Zakup
        fields = ('category', 'month', 'name', 'price')

