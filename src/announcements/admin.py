from django.contrib import admin
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    """ Announcement Model for admin """
    ordering = ('-date_time', )
    list_display = (
        'title',
        'region',
        'place',
        'date_time')
    list_filter = ('region', 'place', 'date_time')
    search_fields = ['title']


admin.site.register(Announcement, AnnouncementAdmin)
