from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from places.models import Place


class AnnouncementsCreateFilter(forms.Form):
    """ Announcements Filter """
    place = forms.ChoiceField(
        label=_('Place'),
        widget=forms.Select(attrs={'onchange': 'form.submit();'}))

    def __init__(self, request, *args, **kwargs):
        super(AnnouncementsCreateFilter, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        places = Place.objects.filter(region=region, is_closed=False)

        PLACE_CHOICES = [(str(place.id), place.name) for place in places]
        self.fields['place'].choices = PLACE_CHOICES
