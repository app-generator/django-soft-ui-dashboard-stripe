from django import forms

from apps.ecommerce.models import Products, Sales


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SaleForm(forms.ModelForm):

    class Meta:
        model = Sales
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
