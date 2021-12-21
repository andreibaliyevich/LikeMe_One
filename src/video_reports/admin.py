from django.contrib import admin
from .models import VideoReport, VideoLike


class VideoReportAdmin(admin.ModelAdmin):
    """ VideoReport Model for admin """
    ordering = ('-date', )
    list_display = (
        'title',
        'author',
        'region',
        'place',
        'date')
    list_filter = ('author', 'region', 'place', 'date')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title', )}


class VideoLikeAdmin(admin.ModelAdmin):
    """ VideoLike Model for admin """
    ordering = ('-id', )
    list_display = (
        'user',
        'video_report',
        'is_like')
    list_filter = ('user', )


admin.site.register(VideoReport, VideoReportAdmin)
admin.site.register(VideoLike, VideoLikeAdmin)
