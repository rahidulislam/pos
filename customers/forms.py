from django import forms
from customers.models import Customer

class CreateCustomerForm(forms.ModelForm):
    """Form definition for Customer."""

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-group'})
        self.fields['email'].widget.attrs.update({'class': 'form-group'})
        self.fields['phone'].widget.attrs.update({'class': 'form-group'})
        self.fields['address'].widget.attrs.update({'class': 'form-group'})

    class Meta:
        """Meta definition for Customerform."""

        model = Customer
        exclude = ('created',)

class UpdateCustomerForm(forms.ModelForm):
    """Form definition for Customer."""

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-group'})
        self.fields['email'].widget.attrs.update({'class': 'form-group'})
        self.fields['phone'].widget.attrs.update({'class': 'form-group'})
        self.fields['address'].widget.attrs.update({'class': 'form-group'})

    class Meta:
        """Meta definition for Customerform."""

        model = Customer
        exclude = ('created',)
