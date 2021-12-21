from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from places.models import Place
from .forms import AnnouncementsCreateFilter
from .models import Announcement


def announcements_list(request):
    """ announcements list """
    region = get_object_or_404(Region, slug=request.session['user_region'])
    announcements_filter = AnnouncementsCreateFilter(request, request.GET or None)

    if request.method == 'GET' and announcements_filter.is_valid():
        announcements_filter_cd = announcements_filter.cleaned_data
        place_id = int(announcements_filter_cd['place'])
        place = get_object_or_404(Place, id=place_id)

        announcements = Announcement.objects.filter(
            place=place, date_time__gt=timezone.now())
    else:
        announcements = Announcement.objects.filter(
            region=region, date_time__gt=timezone.now())

    paginator = Paginator(announcements, 9)
    page_number = request.GET.get('page', 1)
    announcements_page = paginator.get_page(page_number)

    context = {
        'announcements_page': announcements_page,
        'announcements_filter': announcements_filter,
    }
    return render(request, 'announcements/list.html', context)
