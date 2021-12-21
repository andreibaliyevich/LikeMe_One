from os.path import splitext
from django.utils import timezone


def get_place_path(instance, filename):
    timestamp = timezone.now().timestamp()
    file_ext = splitext(filename)[1]
    return f'places/{ timestamp }{ file_ext }'


def get_watermark_path(instance, filename):
    timestamp = timezone.now().timestamp()
    file_ext = splitext(filename)[1]
    return f'watermarks/{ timestamp }{ file_ext }'
