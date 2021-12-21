from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from .models import District, Place


class PlacesCreateFilter(forms.Form):
    """ Places Filter """
    TYPE_PLACE_CHOICES = [
        ('bar', _('Bar')),
        ('bowling', _('Bowling')),
        ('veranda', _('Veranda')),
        ('health', _('Health (or fitness)')),
        ('hookah', _('Hookah')),
        ('karaoke', _('Karaoke')),
        ('coffee_house', _('Coffee House')),
        ('store', _('Store')),
        ('night_club', _('Night Club')),
        ('educational_project', _('Educational Project')),
        ('brewery', _('Brewery')),
        ('entertainment', _('Entertainment (various events)')),
        ('restaurant', _('Restaurant')),
        ('strip_club', _('Strip Club')),
    ]
    type_place = forms.ChoiceField(
        choices=TYPE_PLACE_CHOICES,
        widget=forms.Select(attrs={'onchange': 'form.submit();'}))

    district_place = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange': 'form.submit();'}))

    KITCHEN_PLACE_CHOICES = [
        ('kitchen_author', _('Kitchen Author')),
        ('kitchen_azerbaijani', _('Kitchen Azerbaijani')),
        ('kitchen_american', _('Kitchen American')),
        ('kitchen_armenian', _('Kitchen Armenian')),
        ('kitchen_belarusian', _('Kitchen Belarusian')),
        ('kitchen_georgian', _('Kitchen Georgian')),
        ('kitchen_european', _('Kitchen European')),
        ('kitchen_indian', _('Kitchen Indian')),
        ('kitchen_spanish', _('Kitchen Spanish')),
        ('kitchen_italian', _('Kitchen Italian')),
        ('kitchen_mexican', _('Kitchen Mexican')),
        ('kitchen_russian', _('Kitchen Russian')),
        ('kitchen_ukrainian', _('Kitchen Ukrainian')),
        ('kitchen_japanese', _('Kitchen Japanese')),
    ]
    kitchen_place = forms.ChoiceField(
        choices=KITCHEN_PLACE_CHOICES,
        widget=forms.Select(attrs={'onchange': 'form.submit();'}))

    def __init__(self, request, *args, **kwargs):
        super(PlacesCreateFilter, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        districts = District.objects.filter(region=region)

        DISTRICT_PLACE_CHOICES = []
        for district in districts:
            if request.LANGUAGE_CODE == 'en':
                district_choice = (str(district.id), district.name)
            elif request.LANGUAGE_CODE == 'ru':
                district_choice = (str(district.id), district.name_ru)
            elif request.LANGUAGE_CODE == 'uk':
                district_choice = (str(district.id), district.name_uk)
            DISTRICT_PLACE_CHOICES.append((district_choice))

        self.fields['district_place'].choices = DISTRICT_PLACE_CHOICES

        for key in self.fields:
            self.fields[key].required = False
