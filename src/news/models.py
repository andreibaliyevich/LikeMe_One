from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from .utilities import get_news_path


class News(models.Model):
    """ News Model """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='news',
        verbose_name=_('Author'))
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        db_index=True,
        default=1,
        related_name='news',
        verbose_name=_('Region'))
    
    title = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name='Title')
    title_ru = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name='Заглавие')
    title_uk = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name='Назва')
    
    slug = models.SlugField(
        max_length=128,
        db_index=True,
        verbose_name=_('Slug'))
    main_image = models.ImageField(
        upload_to=get_news_path,
        verbose_name=_('Main Image'))
    date_published = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date Published'))

    content = models.TextField(verbose_name='Content')
    content_ru = models.TextField(verbose_name='Cодержание')
    content_uk = models.TextField(verbose_name='Зміст')
    
    tags = TaggableManager(verbose_name=_('Tags'))
    num_views = models.IntegerField(default=0, verbose_name=_('Num Views'))

    class Meta:
        verbose_name = _('One News')
        verbose_name_plural = _('News')
        ordering = ['-date_published']

    def __str__(self):
        if len(self.title) > 50:
            return self.title[:50] + "..."
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('news:news-detail',
            args=[self.id, self.slug])


class Image(models.Model):
    """ Image Model """
    image = models.ImageField(upload_to=get_news_path, verbose_name=_('Image'))
    owner = models.IntegerField(verbose_name=_('Owner'))

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['-id']

    def __str__(self):
        return self.image.name
