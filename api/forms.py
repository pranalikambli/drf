from django import forms
import re

from .models import Category, Products


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=150)
    subcategory_of = forms.CharField(max_length=150, required=False)

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        id = cleaned_data.get('id', None)
        name = cleaned_data.get('name', None)
        subcategory_of = cleaned_data.get('subcategory_of', None)
        if subcategory_of:
            check_name_exist = Category.objects.filter(name__iexact=name.strip().lower(),
                                                   subcategory_of__iexact=subcategory_of.strip().lower())
        else:
            check_name_exist = Category.objects.filter(name__iexact=name.strip().lower())
        if not id and check_name_exist:
            raise forms.ValidationError('This data is already exist!')
        return cleaned_data

class ProductForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=150)
    price = forms.DecimalField(max_digits=20, decimal_places=2)

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        id = cleaned_data.get('id', None)
        name = cleaned_data.get('name', None)

        if name:
            check_name_exist = Products.objects.filter(name__iexact=name.strip().lower())
            if not id and check_name_exist:
                raise forms.ValidationError('This Product is already exist!')

        return cleaned_data