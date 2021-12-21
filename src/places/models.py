from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from .utilities import get_place_path, get_watermark_path


class District(models.Model):
    """ District Model """
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='districts',
        verbose_name=_('Region'))
    name = models.CharField(max_length=32, verbose_name='Name')
    name_ru = models.CharField(max_length=32, verbose_name='Название')
    name_uk = models.CharField(max_length=32, verbose_name='Назва')

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        ordering = ['name']

    def __str__(self):
        return self.name


class Place(models.Model):
    """ Place Model """
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        default=1,
        related_name='places',
        verbose_name=_('Region'))
    name = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name=_('Name'))
    slug = models.SlugField(
        max_length=64,
        db_index=True,
        verbose_name=_('Slug'))

    address = models.CharField(
        blank=True,
        max_length=256,
        verbose_name=_('Address'))
    phone_number = models.CharField(
        blank=True, max_length=32, verbose_name=_('Phone Number'))

    description = models.TextField(blank=True, verbose_name='Description')
    description_ru = models.TextField(blank=True, verbose_name='Описание')
    description_uk = models.TextField(blank=True, verbose_name='Опис')
    
    url_address = models.URLField(blank=True, verbose_name=_('URL Address'))

    image_place = models.ImageField(
        upload_to=get_place_path,
        verbose_name=_('Image Place'))
    image_watermark = models.ImageField(
        blank=True,
        upload_to=get_watermark_path,
        verbose_name=_('Image Watermark'))

    WATERMARK_POSITION_CHOICES = [
        ('1', _('top left')),
        ('2', _('top right')),
        ('3', _('bottom left')),
        ('4', _('bottom middle')),
        ('5', _('bottom right')),
    ]
    watermark_position = models.CharField(
        max_length=1,
        choices=WATERMARK_POSITION_CHOICES,
        default='5',
        verbose_name=_('Watermark Position'))

    WATERMARK_SCALE_CHOICES = [
        (2, '1/2'),
        (4, '1/4'),
        (5, '1/5'),
        (8, '1/8'),
        (10, '1/10'),
        (15, '1/15'),
        (20, '1/20'),
        (25, '1/25'),
    ]
    watermark_scale = models.IntegerField(
        choices=WATERMARK_SCALE_CHOICES,
        default=15,
        verbose_name=_('Watermark Scale'))

    working_hours = models.CharField(
        blank=True,
        max_length=32,
        verbose_name=_('Working Hours'))

    AVERAGE_CHECK_CHOICES = []
    for x in range(100, 3001, 100):
        choice = (str(x), str(x))
        AVERAGE_CHECK_CHOICES.append(choice)
    average_check = models.CharField(
        blank=True,
        max_length=4,
        choices=AVERAGE_CHECK_CHOICES,
        verbose_name=_('Average Check'))

    bank_card = models.BooleanField(default=False, verbose_name=_('Bank Card'))
    wi_fi = models.BooleanField(default=False, verbose_name='Wi-Fi')
    parking = models.BooleanField(default=False, verbose_name=_('Parking'))
    delivery = models.BooleanField(default=False, verbose_name=_('Delivery'))
    catering = models.BooleanField(default=False, verbose_name=_('Catering'))

    bar = models.BooleanField(default=False, verbose_name=_('Bar'))
    hookah = models.BooleanField(default=False, verbose_name=_('Hookah'))
    restaurant = models.BooleanField(default=False, verbose_name=_('Restaurant'))
    night_club = models.BooleanField(default=False, verbose_name=_('Night Club'))
    karaoke = models.BooleanField(default=False, verbose_name=_('Karaoke'))
    veranda = models.BooleanField(default=False, verbose_name=_('Veranda'))
    strip_club = models.BooleanField(default=False, verbose_name=_('Strip Club'))
    brewery = models.BooleanField(default=False, verbose_name=_('Brewery'))
    bowling = models.BooleanField(default=False, verbose_name=_('Bowling'))
    coffee_house = models.BooleanField(default=False, verbose_name=_('Coffee House'))
    educational_project = models.BooleanField(default=False, verbose_name=_('Educational Project'))
    entertainment = models.BooleanField(default=False, verbose_name=_('Entertainment (various events)'))
    health = models.BooleanField(default=False, verbose_name=_('Health (or fitness)'))
    store = models.BooleanField(default=False, verbose_name=_('Store'))

    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        null=True,
        related_name='places',
        verbose_name=_('District'))

    kitchen_european = models.BooleanField(default=False, verbose_name=_('Kitchen European'))
    kitchen_american = models.BooleanField(default=False, verbose_name=_('Kitchen American'))
    kitchen_italian = models.BooleanField(default=False, verbose_name=_('Kitchen Italian'))
    kitchen_author = models.BooleanField(default=False, verbose_name=_('Kitchen Author'))
    kitchen_ukrainian = models.BooleanField(default=False, verbose_name=_('Kitchen Ukrainian'))
    kitchen_belarusian = models.BooleanField(default=False, verbose_name=_('Kitchen Belarusian'))
    kitchen_russian = models.BooleanField(default=False, verbose_name=_('Kitchen Russian'))
    kitchen_armenian = models.BooleanField(default=False, verbose_name=_('Kitchen Armenian'))
    kitchen_azerbaijani = models.BooleanField(default=False, verbose_name=_('Kitchen Azerbaijani'))
    kitchen_georgian = models.BooleanField(default=False, verbose_name=_('Kitchen Georgian'))
    kitchen_spanish = models.BooleanField(default=False, verbose_name=_('Kitchen Spanish'))
    kitchen_mexican = models.BooleanField(default=False, verbose_name=_('Kitchen Mexican'))
    kitchen_japanese = models.BooleanField(default=False, verbose_name=_('Kitchen Japanese'))
    kitchen_indian = models.BooleanField(default=False, verbose_name=_('Kitchen Indian'))

    place_day = models.BooleanField(default=False, verbose_name=_('Place Day'))

    is_closed = models.BooleanField(default=False, verbose_name=_('Is Closed'))

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('places:place-detail',
            args=[self.id, self.slug])
