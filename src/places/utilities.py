from os.path import splitext
from django.utils import timezone


def get_place_path(instance, filename):
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'places/{ path_name }{ file_ext }'


def get_watermark_path(instance, filename):
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'watermarks/{ path_name }{ file_ext }'
