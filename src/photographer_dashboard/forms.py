from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from places.models import Place
from photo_reports.models import PhotoReport, Photo
from video_reports.models import VideoReport


class PhotoReportForm(forms.ModelForm):
    """ PhotoReport Form """
    class Meta:
        model = PhotoReport
        fields = [
            'author',
            'authors',
            'place',
            'date',
            'title',
            'pay_to_photographer',
            'pay_to_portal',
            'is_plus_18',
            'is_posted',
        ]

    def __init__(self, request, *args, **kwargs):
        super(PhotoReportForm, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        authors = User.objects.filter(
            user_access__region=region, user_access__is_photographer=True)
        places = Place.objects.filter(region=region, is_closed=False)

        AUTHOR_CHOICES = []
        for author in authors:
            if author.get_full_name():
                AUTHOR_CHOICES.append((str(author.id), author.get_full_name()))
            else:
                AUTHOR_CHOICES.append((str(author.id), author.get_username()))
        
        self.fields['author'].choices = AUTHOR_CHOICES
        self.fields['author'].label = _('Primary Photographer')
        
        self.fields['authors'].choices = AUTHOR_CHOICES
        self.fields['authors'].label = _('More Photographers')
        self.fields['authors'].help_text = _('Hold down "Control", or "Command" on a Mac, to select more than one.')

        PLACE_CHOICES = [(str(place.id), place.name) for place in places]
        self.fields['place'].choices = PLACE_CHOICES

        if request.LANGUAGE_CODE == 'en':
            self.fields['date'].widget = DatePickerInput(format='%Y-%m-%d')
        elif request.LANGUAGE_CODE == 'ru' or request.LANGUAGE_CODE == 'uk':
            self.fields['date'].widget = DatePickerInput(format='%d.%m.%Y')


class PhotosForm(forms.ModelForm):
    """ Photos Form """
    image = forms.ImageField(
        label=_('Image'),
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('jpg', 'png'))],
        error_messages={
            'invalid_extension': _('This file format is not supported.')},
        widget=forms.widgets.ClearableFileInput(attrs={'multiple': True}),
        required=False)

    class Meta:
        model = Photo
        fields = ['image']


class VideoReportForm(forms.ModelForm):
    """ VideoReport Form """
    image = forms.ImageField(
        label=_('Image'),
        help_text=_('The minimum image size should be 477x373!'),
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('jpg', 'png'))],
        error_messages={
            'invalid_extension': _('This file format is not supported.')})

    class Meta:
        model = VideoReport
        fields = [
            'author',
            'place',
            'date',
            'title',
            'pay_to_photographer',
            'pay_to_portal',
            'image',
            'url_address',
        ]

    def __init__(self, request, *args, **kwargs):
        super(VideoReportForm, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        authors = User.objects.filter(
            user_access__region=region, user_access__is_photographer=True)
        places = Place.objects.filter(region=region, is_closed=False)

        AUTHOR_CHOICES = []
        for author in authors:
            if author.get_full_name():
                AUTHOR_CHOICES.append((str(author.id), author.get_full_name()))
            else:
                AUTHOR_CHOICES.append((str(author.id), author.get_username()))
        self.fields['author'].choices = AUTHOR_CHOICES

        PLACE_CHOICES = [(str(place.id), place.name) for place in places]
        self.fields['place'].choices = PLACE_CHOICES

        if request.LANGUAGE_CODE == 'en':
            self.fields['date'].widget = DatePickerInput(format='%Y-%m-%d')
        elif request.LANGUAGE_CODE == 'ru' or request.LANGUAGE_CODE == 'uk':
            self.fields['date'].widget = DatePickerInput(format='%d.%m.%Y')
