from django.contrib import admin
from .models import Region, UserAccess, Banner, PhotographerOrder


class RegionAdmin(admin.ModelAdmin):
    """ Region Model for admin """
    ordering = ('id', )
    list_display = ('name', 'id')
    prepopulated_fields = {'slug': ('name', )}


class UserAccessAdmin(admin.ModelAdmin):
    """ User Access Model for admin """
    ordering = ('id', )
    list_display = ('id', 'user', 'region', 'is_admin', 'is_photographer')
    list_filter = ('user', 'region', 'is_admin', 'is_photographer')
    list_editable = ('is_admin', 'is_photographer')


class BannerAdmin(admin.ModelAdmin):
    """ Banner Model for admin """
    ordering = ('type_banner', )
    list_display = ('title', 'region', 'type_banner', 'url_address', 'date')


class PhotographerOrderAdmin(admin.ModelAdmin):
    """ PhotographerOrder Model for admin """
    ordering = ('-id', )
    list_display = ('id', 'region', 'name', 'date', 'address', 'phone_number')


admin.site.register(Region, RegionAdmin)
admin.site.register(UserAccess, UserAccessAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(PhotographerOrder, PhotographerOrderAdmin)
