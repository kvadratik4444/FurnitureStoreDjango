import re
from django import forms
from django.core.exceptions import ValidationError


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[('0', 'False'), ('1', 'True')])
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[('0', 'False'), ('1', 'True')])

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number.isdigit():
            raise ValidationError("Номер телефона должен содержать только цифры.")

        if len(phone_number) != 10:
            raise ValidationError("Номер телефона должен содержать 10 цифр.")

        if not re.match(r'^9\d{9}$', phone_number):
            raise ValidationError("Номер телефона должен начинаться с 9 и содержать 10 цифр.")

        return phone_number
