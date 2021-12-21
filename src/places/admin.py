from django.contrib import admin
from .models import District, Place


class DistrictAdmin(admin.ModelAdmin):
    """ District Model for admin """
    ordering = ('name', )
    list_display = ('name', 'region')
    list_filter = ('region', )


class PlaceAdmin(admin.ModelAdmin):
    """ Place Model for admin """
    ordering = ('name', )
    list_display = (
        'name', 
        'region',
        'address',
        'phone_number',
        'working_hours',
        'average_check',
        'district',
        'place_day',
        'is_closed')
    list_filter = (
        'region',
        'district')
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(District, DistrictAdmin)
admin.site.register(Place, PlaceAdmin)
