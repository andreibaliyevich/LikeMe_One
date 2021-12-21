from os.path import splitext
from django.utils import timezone


def get_banner_path(instance, filename):
    timestamp = timezone.now().timestamp()
    file_ext = splitext(filename)[1]
    return f'banners/{ timestamp }{ file_ext }'
