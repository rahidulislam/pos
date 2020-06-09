from django import forms
from products.models import Products
from branches.models import Branch

class CreateProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sku_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': 1})
        self.fields['manufacturer'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['product_image'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Products
        exclude = ['created','updated', 'quantity', 'buying_price', 'wholesale_price', 'retail_price']

class UpdateProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sku_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': 1})
        self.fields['manufacturer'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['buying_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['retail_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['wholesale_price'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Products
        exclude = ['created', 'updated',]

class TransferFiltersForm(forms.Form):
    date_from = forms.DateTimeField()
    date_to = forms.DateTimeField()
    transfered_from = forms.ModelChoiceField(queryset=Branch.objects.all())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_from'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_from'].widget.attrs.update({'id': 'date_from'})
        self.fields['date_from'].widget.attrs.update({'placeholder': 'Date from'})
        self.fields['date_to'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_to'].widget.attrs.update({'id': 'date_to'})
        self.fields['date_to'].widget.attrs.update({'placeholder': 'Date to'})
        self.fields['transfered_from'].widget.attrs.update({'class': 'form-control'})

class SetTransferToForm(forms.Form):
    transfer_to = forms.ModelChoiceField(queryset=Branch.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transfer_to'].widget.attrs.update({'class': 'form-control'})


class ProductTransferForm(forms.Form):
    product = forms.CharField(max_length=100)
    quantity = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['product'].widget.attrs.update({'id': 'product_id'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
    



