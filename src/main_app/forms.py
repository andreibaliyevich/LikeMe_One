from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from .models import PhotographerOrder


class PhotographerOrderForm(forms.ModelForm):
    """ PhotographerOrder Form """
    class Meta:
        model = PhotographerOrder
        fields = ['name', 'date', 'address', 'phone_number']

    def __init__(self, request, *args, **kwargs):
        super(PhotographerOrderForm, self).__init__(*args, **kwargs)

        if request.LANGUAGE_CODE == 'en':
            self.fields['date'].widget = DatePickerInput(format='%Y-%m-%d')
        elif request.LANGUAGE_CODE == 'ru' or request.LANGUAGE_CODE == 'uk':
            self.fields['date'].widget = DatePickerInput(format='%d.%m.%Y')
