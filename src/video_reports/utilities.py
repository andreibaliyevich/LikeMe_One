from os.path import splitext
from django.utils import timezone


def get_videoreport_path(instance, filename):
    file_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1]
    return f'videoreports/{ file_name }{ file_ext }'
