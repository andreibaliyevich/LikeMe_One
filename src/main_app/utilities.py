from os.path import splitext
from django.utils import timezone


def get_banner_path(instance, filename):
    path_name = timezone.now().timestamp()
    file_ext = splitext(filename)[1].lower()
    return f'banners/{ path_name }{ file_ext }'
