from tinymce.widgets import TinyMCE
from django.contrib import admin
from django.db import models
from .models import News, Image


class NewsAdmin(admin.ModelAdmin):
    """ News Model for admin """
    ordering = ('-date_published', )
    list_display = (
        'title',
        'author',
        'region',
        'date_published')
    list_filter = ('author', 'region', 'date_published')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


class ImageAdmin(admin.ModelAdmin):
    """ Image Model for admin """
    ordering = ('-id', )
    list_display = ('id', 'image', 'owner')


admin.site.register(News, NewsAdmin)
admin.site.register(Image, ImageAdmin)
