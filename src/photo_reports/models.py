from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from places.models import Place
from .utilities import get_cover_path, get_photo_path, get_thumbnail_path


class PhotoReport(models.Model):
    """ PhotoReport Model """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='photoreports',
        verbose_name=_('Author'))
    authors = models.ManyToManyField(
        User,
        blank=True,
        verbose_name=_('Authors'))
    
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        default=1,
        related_name='photoreports',
        verbose_name=_('Region'))
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        db_index=True,
        default=1,
        related_name='photoreports',
        verbose_name=_('Place'))
    date = models.DateField(
        default=timezone.now,
        verbose_name=_('Date'))
    title = models.CharField(
        db_index=True,
        max_length=128,
        default='new photo report',
        verbose_name=_('Title'))
    slug = models.SlugField(
        db_index=True,
        max_length=128,
        default='new-photo-report',
        verbose_name=_('Slug'))
    pay_to_photographer = models.IntegerField(
        db_index=True,
        default=0,
        verbose_name=_('Pay to Photographer'))
    pay_to_portal = models.IntegerField(
        db_index=True,
        default=0,
        verbose_name=_('Pay to Portal'))
    main_image = ThumbnailerImageField(
        upload_to=get_cover_path,
        resize_source={
            'size': (477, 373),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        default='covers/hidden.jpg',
        verbose_name=_('Main Image'))
    is_plus_18 = models.BooleanField(default=False, verbose_name='+18')
    is_posted = models.BooleanField(default=False, verbose_name=_('Is Posted'))
    num_views = models.IntegerField(default=0, verbose_name=_('Num Views'))

    class Meta:
        verbose_name = _('Photoreport')
        verbose_name_plural = _('Photoreports')
        ordering = ['-date']

    def __str__(self):
        if len(self.title) > 50:
            return self.title[:50] + "..."
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('photo_reports:photo-report-detail',
            args=[self.id, self.slug])


class Photo(models.Model):
    """ Photo Model """
    photo_report = models.ForeignKey(
        PhotoReport,
        on_delete=models.CASCADE,
        related_name='photos')
    image = models.ImageField(
        upload_to=get_photo_path,
        verbose_name=_('Image'))
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumbnail_path,
        resize_source={
            'size': (350, 235),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        blank=True,
        verbose_name=_('Thumbnail'))
    is_available = models.BooleanField(default=True, verbose_name=_('Is Available'))
    is_cover = models.BooleanField(default=False, verbose_name=_('Is Cover'))

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __str__(self):
        return str(self.id)


class PhotoLike(models.Model):
    """ PhotoLike Model """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='photo_like',
        verbose_name=_('User'))
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='photo_like',
        verbose_name=_('Photo'))
    is_like = models.BooleanField(default=True, verbose_name=_('Is like'))

    class Meta:
        verbose_name = _('Photo Like')
        verbose_name_plural = _('Photo Likes')
        ordering = ['-id']
        unique_together = [['user', 'photo']]

    def __str__(self):
        return str(self.id)
