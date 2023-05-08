from django import forms
from .models import Book,Payment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Button,Submit
class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields ="__all__"

        """def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.helper=FormHelper(self)
            self.helper.layout=Layout('title','price',Submit('Buy',css_class='button white btn-block btn-primary'))"""
        
class PaymentForm(forms.ModelForm):
    helper=FormHelper()
    class Meta:
        model=Payment
        fields="__all__"