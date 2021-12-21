from easy_thumbnails.fields import ThumbnailerImageField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from places.models import Place
from .utilities import get_announcement_path


class Announcement(models.Model):
    """ Announcement Model """
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        default=1,
        related_name='announcements',
        verbose_name=_('Region'))
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='announcements',
        verbose_name=_('Place'))
    title = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('Title'))
    image = ThumbnailerImageField(
        upload_to=get_announcement_path,
        resize_source={
            'size': (640, 0),
            'crop': 'scale',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Image'))
    date_time = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date/Time'))

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
        ordering = ['date_time']

    def __str__(self):
        if len(self.title) > 50:
            return self.title[:50] + "..."
        else:
            return self.title
