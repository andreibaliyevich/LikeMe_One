from django.contrib import admin
from .models import PhotoReport, Photo, PhotoLike


class PhotoInline(admin.TabularInline):
    model = Photo


class PhotoReportAdmin(admin.ModelAdmin):
    """ PhotoReport Model for admin """
    ordering = ('-date', )
    list_display = (
        'title',
        'author',
        'region',
        'place',
        'date',
        'is_posted')
    list_filter = ('author', 'region', 'place', 'date')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title', )}
    inlines = [PhotoInline]


class PhotoLikeAdmin(admin.ModelAdmin):
    """ PhotoLike Model for admin """
    ordering = ('-id', )
    list_display = (
        'user',
        'photo',
        'is_like')
    list_filter = ('user', )


admin.site.register(PhotoReport, PhotoReportAdmin)
admin.site.register(PhotoLike, PhotoLikeAdmin)
