from os.path import splitext
from django.utils import timezone


def get_cover_path(instance, filename):
    file_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1]
    return f'covers/{ file_name }{ file_ext }'


def get_photo_path(instance, filename):
    file_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1]
    return f'photos/{ file_name }{ file_ext }'


def get_thumbnail_path(instance, filename):
    file_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1]
    return f'thumbnails/{ file_name }{ file_ext }'
