from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _
from announcements.models import Announcement
from news.models import News
from places.models import Place
from photo_reports.models import PhotoReport, Photo, PhotoLike
from video_reports.models import VideoReport
from .forms import PhotographerOrderForm
from .models import Region, Banner


def index(request):
    """ homepage """
    region = get_object_or_404(Region, slug=request.session['user_region'])

    banners = Banner.objects.filter(region=region)
    announcements = Announcement.objects.filter(
        region=region, date_time__gt=timezone.now())
    news = News.objects.filter(region=region)[:2]
    places = Place.objects.filter(region=region, place_day=True)[:4]

    if banners.filter(type_banner='#5').exists():
        photo_reports = PhotoReport.objects.filter(
            region=region, is_posted=True)[:8]
    else:
        photo_reports = PhotoReport.objects.filter(
            region=region, is_posted=True)[:9]

    photo_reports_tuples = []
    for photo_report in photo_reports:
        photo_report_likes_count = PhotoLike.objects.filter(
            photo__photo_report=photo_report, is_like=True).count()
        photo_reports_tuples.append((photo_report, photo_report_likes_count))

    context = {
        'banners': banners,
        'announcements': announcements,
        'news': news,
        'places': places,
        'photo_reports_tuples': photo_reports_tuples,
    }
    return render(request, 'main_app/index.html', context)


def search(request):
    """ search """
    region = get_object_or_404(Region, slug=request.session['user_region'])

    photo_reports = PhotoReport.objects.filter(region=region)
    video_reports = VideoReport.objects.filter(region=region)
    places = Place.objects.exclude(id=1).filter(region=region)
    news = News.objects.filter(region=region)

    query = request.GET.get('q', '')

    if query:
        photo_reports_found = photo_reports.filter(
            Q(title__icontains=query)
            & Q(is_posted=True)
        )
        video_reports_found = video_reports.filter(Q(title__icontains=query))
        places_found = places.filter(
            Q(name__icontains=query)
            | Q(address__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(description__icontains=query)
            | Q(description_ru__icontains=query)
            | Q(description_uk__icontains=query),
            Q(is_closed=False)
        )
        news_found = news.filter(
            Q(title__icontains=query)
            | Q(title_ru__icontains=query)
            | Q(title_uk__icontains=query)
            | Q(content__icontains=query)
            | Q(content_ru__icontains=query)
            | Q(content_uk__icontains=query)
        )
    else:
        photo_reports_found = []
        video_reports_found = []
        places_found = []
        news_found = []

    context = {
        'news_found': news_found,
        'places_found': places_found,
        'photo_reports_found': photo_reports_found,
        'video_reports_found': video_reports_found,
    }
    return render(request, 'main_app/search.html', context)


def photographer_order(request):
    """ photographer order """
    photographer_order_form = PhotographerOrderForm(request, request.POST or None)

    context = {
        'photographer_order_form': photographer_order_form,
    }

    if request.method == 'POST' and photographer_order_form.is_valid():
        photographer_order_form_save = photographer_order_form.save(commit=False)
        photographer_order_form_save.region = get_object_or_404(
            Region, slug=request.session['user_region'])
        photographer_order_form_save.save()
        
        context['message'] = 'Your order has been sent!'
        return render(request, 'main_app/photographer-order.html', context)
    else:
        return render(request, 'main_app/photographer-order.html', context)


def register(request):
    """ register user """
    if request.user.is_authenticated:
        return redirect('main_app:index')

    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, 
                password=request.POST['password1'])
            login(request, authenticated_user)
            return redirect('main_app:index')
    context = { 'form': form }
    return render(request, 'main_app/users/register.html', context)


def set_region(request, region_slug):
    """ set region """
    request.session['user_region'] = region_slug
    return redirect('main_app:index')

def set_language(request, language_code):
    """ set language """
    activate(language_code)
    return redirect('main_app:index')


def about(request):
    """ about """
    return render(request, 'main_app/about.html')


def policy(request):
    """ policy """
    return render(request, 'main_app/policy.html')


def vacancy(request):
    """ vacancy """
    return render(request, 'main_app/vacancy.html')


def error_400(request, exception):
    return render(request, 'main_app/error/400.html', status=400)


def error_403(request, exception):
    return render(request, 'main_app/error/403.html', status=403)


def error_404(request, exception):
    return render(request, 'main_app/error/404.html', status=404)


def error_500(request):
    return render(request, 'main_app/error/500.html', status=500)
