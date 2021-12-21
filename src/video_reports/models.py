from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from places.models import Place
from .utilities import get_videoreport_path


class VideoReport(models.Model):
    """ VideoReport Model """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='videoreports',
        verbose_name=_('Author'))
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        default=1,
        related_name='videoreports',
        verbose_name=_('Region'))
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='videoreports',
        verbose_name=_('Place'))
    date = models.DateField(
        default=timezone.now,
        verbose_name=_('Date'))
    title = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('Title'))
    slug = models.SlugField(
        max_length=128,
        db_index=True,
        verbose_name=_('Slug'))
    pay_to_photographer = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name=_('Pay to Photographer'))
    pay_to_portal = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name=_('Pay to Portal'))
    image = models.ImageField(
        upload_to=get_videoreport_path,
        verbose_name=_('Image'))
    url_address = models.URLField(
        verbose_name=_('URL Address'))
    num_views = models.IntegerField(default=0, verbose_name=_('Num Views'))

    class Meta:
        verbose_name = _('Videoreport')
        verbose_name_plural = _('Videoreports')
        ordering = ['-date']

    def __str__(self):
        if len(self.title) > 50:
            return self.title[:50] + "..."
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('video_reports:video-report-detail',
            args=[self.id, self.slug])


class VideoLike(models.Model):
    """ VideoLike Model """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='video_like',
        verbose_name=_('User'))
    video_report = models.ForeignKey(
        VideoReport,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='video_like',
        verbose_name=_('Videoreport'))
    is_like = models.BooleanField(default=True, verbose_name=_('Is like'))

    class Meta:
        verbose_name = _('Video Like')
        verbose_name_plural = _('Video Likes')
        ordering = ['-id']
        unique_together = [['user', 'video_report']]

    def __str__(self):
        return str(self.id)
