from datetime import datetime
from bootstrap_datepicker_plus import DateTimePickerInput
from tinymce.widgets import TinyMCE
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main_app.models import Region, Banner
from photo_reports.models import PhotoReport
from video_reports.models import VideoReport
from announcements.models import Announcement
from places.models import District, Place
from news.models import News
from .validators import MinSizeImageValidator


class DateForm(forms.Form):
    """ Date Form """
    date = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange': 'form.submit();'}))

    def __init__(self, request, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        photo_reports = PhotoReport.objects.filter(region=region)
        video_reports = VideoReport.objects.filter(region=region)
        
        DATE_CHOICES = []
        DATE_CHOICES.append(
            (f'{ datetime.now().year }-{ datetime.now().month }',
            f'{ datetime.now().year }-{ datetime.now().month }')
        )
        
        for photo_report in photo_reports:
            date_choice = (
                (f'{ photo_report.date.year }-{ photo_report.date.month }',
                f'{ photo_report.date.year }-{ photo_report.date.month }')
            )
            if date_choice not in DATE_CHOICES:
                DATE_CHOICES.append(date_choice)

        for video_report in video_reports:
            date_choice = (
                (f'{ video_report.date.year }-{ video_report.date.month }',
                f'{ video_report.date.year }-{ video_report.date.month }')
            )
            if date_choice not in DATE_CHOICES:
                DATE_CHOICES.append(date_choice)

        DATE_CHOICES_SORTED = sorted(
            DATE_CHOICES,
            key=lambda x: datetime.strptime(x[0], '%Y-%m'),
            reverse=True)
        self.fields['date'].choices = DATE_CHOICES_SORTED


class BannerForm(forms.ModelForm):
    """ Banner Form """
    class Meta:
        model = Banner
        fields = ['title', 'type_banner', 'image', 'url_address']


class AnnouncementForm(forms.ModelForm):
    """ Announcement Form """
    class Meta:
        model = Announcement
        fields = ['place', 'title', 'image', 'date_time']

    def __init__(self, request, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        places = Place.objects.filter(region=region, is_closed=False)

        PLACE_CHOICES = [(str(place.id), place.name) for place in places]
        self.fields['place'].choices = PLACE_CHOICES

        if request.LANGUAGE_CODE == 'en':
            self.fields['date_time'].widget = DateTimePickerInput(
                format='%Y-%m-%d %H:%M:%S')
        elif request.LANGUAGE_CODE == 'ru' or request.LANGUAGE_CODE == 'uk':
            self.fields['date_time'].widget = DateTimePickerInput(
                format='%d.%m.%Y %H:%M:%S')


class PlaceForm(forms.ModelForm):
    """ Place Form """
    image_place = forms.ImageField(
        label=_('Image Place'),
        help_text=_('The minimum image size should be 477x373!'),
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('jpg', 'png')),
            MinSizeImageValidator(477, 373),
        ],
        error_messages={
            'invalid_extension': _('This file format is not supported.')})

    image_watermark = forms.ImageField(
        label=_('Image Watermark'),
        help_text=_('Uploading image must be in png format!'),
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('png', ))],
        error_messages={
            'invalid_extension': _('This file format is not supported.')},
        required=False)

    WORKING_HOURS_CHOICES = [
        ("o'clock", _("O'clock")),
        ('24/7', _('24/7')),
    ]
    working_hours = forms.ChoiceField(
        label=_('Working Hours'),
        choices=WORKING_HOURS_CHOICES,
        widget=forms.RadioSelect,
        required=False)
    
    HOUR_CHOICES = [(f'{x}', f'{x}') for x in range(1, 25)]
    from_hour = forms.ChoiceField(
        label=_('from'),
        choices=HOUR_CHOICES,
        initial='1')
    to_hour = forms.ChoiceField(
        label=_('to'),
        choices=HOUR_CHOICES,
        initial='1')

    CHOICES = [(True, _('Yes')), (False, _('No'))]

    bank_card = forms.ChoiceField(
        label=_('Bank Card'),
        choices=CHOICES,
        widget=forms.RadioSelect,
        required=False)
    wi_fi = forms.ChoiceField(
        label='Wi-Fi',
        choices=CHOICES,
        widget=forms.RadioSelect,
        required=False)
    parking = forms.ChoiceField(
        label=_('Parking'),
        choices=CHOICES,
        widget=forms.RadioSelect,
        required=False)
    delivery = forms.ChoiceField(
        label=_('Delivery'),
        choices=CHOICES,
        widget=forms.RadioSelect,
        required=False)
    catering = forms.ChoiceField(
        label=_('Catering'),
        choices=CHOICES,
        widget=forms.RadioSelect,
        required=False)

    PLACE_DAY_CHOICES = [
        (False, _('Not chosen')),
        (True, _('Add')),
        (False, _('Exclude')),
    ]
    place_day = forms.ChoiceField(
        label=_('Place Day'),
        choices=PLACE_DAY_CHOICES,
        initial=False,
        widget=forms.RadioSelect)

    class Meta:
        model = Place
        fields = [
            'name',
            'address',
            'phone_number',
            'description',
            'description_ru',
            'description_uk',
            'url_address',
            'image_place',
            'image_watermark',
            'watermark_position',
            'watermark_scale',
            'working_hours',
            'from_hour',
            'to_hour',
            'average_check',
            'bank_card',
            'wi_fi',
            'parking',
            'delivery',
            'catering',
            'bar',
            'hookah',
            'restaurant',
            'night_club',
            'karaoke',
            'veranda',
            'strip_club',
            'brewery',
            'bowling',
            'coffee_house',
            'educational_project',
            'entertainment',
            'health',
            'store',
            'district',
            'kitchen_european',
            'kitchen_american',
            'kitchen_italian',
            'kitchen_author',
            'kitchen_ukrainian',
            'kitchen_belarusian',
            'kitchen_russian',
            'kitchen_armenian',
            'kitchen_azerbaijani',
            'kitchen_georgian',
            'kitchen_spanish',
            'kitchen_mexican',
            'kitchen_japanese',
            'kitchen_indian',
            'place_day',
            'is_closed',
        ]

    def __init__(self, request, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        districts = District.objects.filter(region=region)

        DISTRICT_PLACE_CHOICES = []
        DISTRICT_PLACE_CHOICES.append(('', '----------'))
        for district in districts:
            if request.LANGUAGE_CODE == 'en':
                district_choice = (str(district.id), district.name)
            elif request.LANGUAGE_CODE == 'ru':
                district_choice = (str(district.id), district.name_ru)
            elif request.LANGUAGE_CODE == 'uk':
                district_choice = (str(district.id), district.name_uk)
            
            if district_choice not in DISTRICT_PLACE_CHOICES:
                DISTRICT_PLACE_CHOICES.append(district_choice)
        self.fields['district'].choices = DISTRICT_PLACE_CHOICES


class NewsForm(forms.ModelForm):
    """ News Form """
    main_image = forms.ImageField(
        label=_('Main Image'),
        help_text=_('The minimum image size should be 471x319!'),
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=('jpg', 'png')),
            MinSizeImageValidator(471, 319),
        ],
        error_messages={
            'invalid_extension': _('This file format is not supported.')})

    content = forms.CharField(label='Content', widget=TinyMCE)
    content_ru = forms.CharField(label='Cодержание', widget=TinyMCE)
    content_uk = forms.CharField(label='Зміст', widget=TinyMCE)

    class Meta:
        model = News
        fields = [
            'author',
            'title',
            'title_ru',
            'title_uk',
            'main_image',
            'content',
            'content_ru',
            'content_uk',
            'tags',
        ]

    def __init__(self, request, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        authors = User.objects.filter(
            user_access__region=region, user_access__is_admin=True)

        AUTHOR_CHOICES = []
        for author in authors:
            if author.get_full_name():
                AUTHOR_CHOICES.append((str(author.id), author.get_full_name()))
            else:
                AUTHOR_CHOICES.append((str(author.id), author.get_username()))

        self.fields['author'].choices = AUTHOR_CHOICES
