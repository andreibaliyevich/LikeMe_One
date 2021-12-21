from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utilities import get_banner_path


class Region(models.Model):
    """ Region Model """
    name = models.CharField(
        db_index=True,
        max_length=32,
        verbose_name='Name')
    name_ru = models.CharField(
        db_index=True,
        max_length=32,
        verbose_name='Название')
    name_uk = models.CharField(
        db_index=True,
        max_length=32,
        verbose_name='Назва')
    slug = models.SlugField(
        db_index=True,
        max_length=32,
        unique=True,
        verbose_name=_('Slug'))

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        ordering = ['id']

    def __str__(self):
        return self.name


class UserAccess(models.Model):
    """ User Access Model """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='user_access',
        verbose_name=_('User'))
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='user_access',
        verbose_name=_('Region'))

    is_admin = models.BooleanField(default=False, verbose_name=_('Is Admin'))
    is_photographer = models.BooleanField(default=False, verbose_name=_('Is Photographer'))

    class Meta:
        verbose_name = _('User Access')
        verbose_name_plural = _('Users Access')
        ordering = ['id']
        unique_together = [['user', 'region']]

    def __str__(self):
        return str(self.id)


class Banner(models.Model):
    """ Banner Model """
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='banners',
        verbose_name=_('Region'))
    title = models.CharField(
        db_index=True,
        max_length=128,
        default='Banner',
        verbose_name=_('Title'))
    TYPE_BANNER_CHOICES = [('#1', '#1'),
                           ('#2', '#2'),
                           ('#3', '#3'),
                           ('#4', '#4'),
                           ('#5', '#5')]
    type_banner = models.CharField(
        max_length=3,
        choices=TYPE_BANNER_CHOICES,
        default='#1',
        verbose_name=_('Type Banner'))
    image = models.ImageField(
        upload_to=get_banner_path, verbose_name=_('Image'))
    url_address = models.URLField(verbose_name=_('URL Address'))
    date = models.DateField(auto_now=True, verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['type_banner']
        unique_together = [['region', 'type_banner']]

    def __str__(self):
        return self.title


class PhotographerOrder(models.Model):
    """ PhotographerOrder Model """
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='photographer_orders',
        verbose_name=_('Region'))
    name = models.CharField(
        db_index=True,
        max_length=32,
        verbose_name=_('Name'))
    date = models.DateField(default=timezone.now, verbose_name=_('Date'))
    address = models.CharField(max_length=256, verbose_name=_('Address'))
    phone_number = models.CharField(
        max_length=32, verbose_name=_('Phone Number'))
    viewed = models.BooleanField(default=False, verbose_name=_('Viewed'))

    class Meta:
        verbose_name = _('Photographer Order')
        verbose_name_plural = _('Photographer Orders')
        ordering = ['-id']

    def __str__(self):
        return str(self.id)
