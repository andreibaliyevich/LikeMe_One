import os, json
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from likeme_one.settings import BASE_DIR, SITE_URL_ADDRESS
from main_app.models import Region
from places.models import Place
from .forms import PhotoReportsCreateFilter
from .models import PhotoReport, Photo, PhotoLike


def photo_reports_list(request):
    """ photo reports list """
    region = get_object_or_404(Region, slug=request.session['user_region'])
    photo_reports_filter = PhotoReportsCreateFilter(request, request.GET or None)

    if request.method == 'GET' and photo_reports_filter.is_valid():
        photo_reports_filter_cd = photo_reports_filter.cleaned_data
        place_id = int(photo_reports_filter_cd['place'])
        place = get_object_or_404(Place, id=place_id)
        
        photo_reports = PhotoReport.objects.filter(place=place, is_posted=True)
    else:
        photo_reports = PhotoReport.objects.filter(region=region, is_posted=True)

    photo_reports_tuples = []
    for photo_report in photo_reports:
        photo_report_likes_count = PhotoLike.objects.filter(
            photo__photo_report=photo_report, is_like=True).count()
        photo_reports_tuples.append((photo_report, photo_report_likes_count))

    paginator = Paginator(photo_reports_tuples, 9)
    page_number = request.GET.get('page', 1)
    photo_reports_page = paginator.get_page(page_number)

    context = {
        'photo_reports_page': photo_reports_page,
        'photo_reports_filter': photo_reports_filter,
    }

    return render(request, 'photo_reports/list.html', context)


def photo_report_detail(request, pr_id, pr_slug):
    """ photo report detail """
    photo_report = get_object_or_404(PhotoReport, id=pr_id, slug=pr_slug)

    if photo_report.is_posted == True:
        likes_count = PhotoLike.objects.filter(
            photo__photo_report=photo_report, is_like=True).count()

        photos = []
        file_json = f'{ BASE_DIR }/media/sequence_photos/{ pr_id }.json'
        if os.path.exists(file_json):
            sequence_photos = []
            with open(file_json, 'r') as file_object:
                sequence_photos = json.load(file_object)
            
            for photo_id in sequence_photos:
                photo = get_object_or_404(Photo, id=photo_id)
                if photo.is_available:
                    photos.append(photo)
        else:
            photos = Photo.objects.filter(
                photo_report=photo_report, is_available=True)

        photo_tuples = []
        for photo in photos:
            photo_likes_count = PhotoLike.objects.filter(
                photo=photo, is_like=True).count()
            try:
                user = User.objects.get(id=request.user.id)
                photo_like = PhotoLike.objects.get(user=user, photo=photo)
                user_is_liked = photo_like.is_like
            except:
                user_is_liked = False
            photo_tuples.append((photo, photo_likes_count, user_is_liked))

        photo_report.num_views += 1
        photo_report.save()

        context = {
            'site_url_address': SITE_URL_ADDRESS,
            'photo_report': photo_report,
            'likes_count': likes_count,
            'photo_tuples': photo_tuples,
        }
        return render(request, 'photo_reports/detail.html', context)
    else:
        raise Http404


@require_POST
def photo_view(request):
    """ photo view """
    photo_report = get_object_or_404(PhotoReport, id=request.POST.get('pr_id'))

    photo_report.num_views += 1
    photo_report.save()

    data = { 'views_count': photo_report.num_views }
    return JsonResponse(data)


@require_POST
def photo_like(request):
    """ photo like """
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))
    user = get_object_or_404(User, id=request.user.id)
    photo_report = get_object_or_404(PhotoReport, id=photo.photo_report.id)

    try:
        add_photo_like = PhotoLike.objects.get(user=user, photo=photo)
        if add_photo_like.is_like:
            add_photo_like.is_like = False
        else:
            add_photo_like.is_like = True
    except:
        add_photo_like = PhotoLike()
        add_photo_like.user = user
        add_photo_like.photo = photo

    add_photo_like.save()

    data = {
        'photo_likes_count': PhotoLike.objects.filter(
            photo=photo, is_like=True).count(),
        'likes_count': PhotoLike.objects.filter(
            photo__photo_report=photo_report, is_like=True).count(),
    }
    return JsonResponse(data)


def download_archive(request, pr_id):
    """ download archive """
    file_name = f'{ BASE_DIR }/media/archives/{ pr_id }.zip'
    return FileResponse(open(file_name, 'rb'), as_attachment=True)
