import os, json, random
from unidecode import unidecode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from likeme_one.settings import BASE_DIR, SITE_NAME
from main_app.context_processors import user_access
from main_app.models import Region
from places.models import Place
from photo_reports.models import PhotoReport, Photo
from video_reports.models import VideoReport
from .forms import PhotoReportForm, PhotosForm, VideoReportForm
from .utilities import paste_watermarks, zip_create


@login_required
def photographer_dashboard(request):
    """ photographer dashboard """
    return redirect('photographer_dashboard:photo-reports')


@login_required
def photo_reports(request):
    """ photo reports """
    if user_access(request)['user_is_photographer']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        photo_reports = PhotoReport.objects.filter(region=region)
        photo_reports = photo_reports.order_by('is_posted', '-date')

        paginator = Paginator(photo_reports, 10)
        page_number = request.GET.get('page', 1)
        photo_reports_page = paginator.get_page(page_number)

        context = {
            'photo_reports_page': photo_reports_page,
        }
        return render(request, 'photographer_dashboard/photo_reports.html', context)
    else:
        raise PermissionDenied


@login_required
def photo_upload(request, pr_id):
    """ photo upload """
    if request.method == 'POST':
        photo_report = get_object_or_404(PhotoReport, id=pr_id)

        photos_form = PhotosForm(request.POST, request.FILES)
        if photos_form.is_valid():
            photo = photos_form.save(commit=False)
            photo.photo_report = photo_report
            photo.thumbnail = File(photo.image)
            photo.save()

            data = {
                'is_valid': True,
                'id': photo.id,
                'image_url': photo.image.url,
                'thumbnail_url': photo.thumbnail.url,
            }
        else:
            data = { 'is_valid': False }

        return JsonResponse(data)


@login_required
def photo_available(request):
    """ photo available """
    if request.method == 'POST':
        photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))

        if photo.is_available:
            photo.is_available = False
        else:
            photo.is_available = True

        photo.save()

        data = {}
        return JsonResponse(data)


@login_required
def photo_cover(request):
    """ photo cover """
    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        photo = get_object_or_404(Photo, id=photo_id)
        photo.is_cover = True
        photo.save()

        photo_report = get_object_or_404(PhotoReport, id=photo.photo_report.id)            
        photo_report.main_image = File(photo.image)
        photo_report.save()

        photos = Photo.objects.filter(photo_report=photo_report)
        photos = photos.exclude(id=photo_id)
        for photo in photos:
            photo.is_cover = False
            photo.save()

        data = {}
        return JsonResponse(data)


@login_required
def shuffle_photos(request):
    """ shuffle photos """
    if request.method == 'POST':
        pr_id = request.POST.get('pr_id')
        photo_report = get_object_or_404(PhotoReport, id=pr_id)
        photos = Photo.objects.filter(photo_report=photo_report)

        sequence_photos = []
        image_url = []
        thumbnail_url = []
        is_available = []
        is_cover = []

        for photo in photos:
            sequence_photos.append(photo.id)

        random.shuffle(sequence_photos)

        file_json = f'{ BASE_DIR }/media/sequence_photos/{ pr_id }.json'
        with open(file_json, 'w') as file_object:
            json.dump(sequence_photos, file_object)

        for photo_id in sequence_photos:
            photo = get_object_or_404(Photo, id=photo_id)
            image_url.append(photo.image.url)
            thumbnail_url.append(photo.thumbnail.url)
            is_available.append(photo.is_available)
            is_cover.append(photo.is_cover)

        data = {
            'sequence_photos': sequence_photos,
            'image_url': image_url,
            'thumbnail_url': thumbnail_url,
            'is_available': is_available,
            'is_cover': is_cover,
        }
        return JsonResponse(data)


@login_required
def add_photo_report(request):
    """ add photo report """
    if user_access(request)['user_is_photographer']:
        user = get_object_or_404(User, id=request.user.id)
        region = get_object_or_404(Region, slug=request.session['user_region'])

        photo_report = PhotoReport(author=user, region=region)
        photo_report.save()

        return redirect(
            'photographer_dashboard:edit-photo-report',
            pr_id=photo_report.id)
    else:
        raise PermissionDenied


@login_required
def add_photo_report_to_place(request, place_id):
    """ add photo report to place """
    if user_access(request)['user_is_photographer']:
        user = get_object_or_404(User, id=request.user.id)
        region = get_object_or_404(Region, slug=request.session['user_region'])
        place = get_object_or_404(Place, id=place_id)

        photo_report = PhotoReport(author=user, region=region, place=place)
        photo_report.save()

        return redirect(
            'photographer_dashboard:edit-photo-report',
            pr_id=photo_report.id)
    else:
        raise PermissionDenied


@login_required
def edit_photo_report(request, pr_id):
    """ edit photo report """
    if user_access(request)['user_is_photographer']:
        photo_report = get_object_or_404(PhotoReport, id=pr_id)

        context = {
            'pr_id': pr_id,
        }

        if request.method == 'POST':
            photo_report_form = PhotoReportForm(
                request, request.POST, request.FILES, instance=photo_report)
            photos_form = PhotosForm(request.POST, request.FILES)

            if photo_report_form.is_valid() and photos_form.is_valid():
                photo_report_cd = photo_report_form.cleaned_data
                photo_report = photo_report_form.save(commit=False)
                photo_report.slug = slugify(unidecode(photo_report_cd['title']))

                try:
                    photo_report.save()
                    photo_report_form.save_m2m()
                except IntegrityError:
                    context['photo_report_form'] = photo_report_form
                    context['photos_form'] = photos_form
                    context['message'] = 'Error!'
                    return render(request, 'photographer_dashboard/edit_photo_report.html', context)

                photos = Photo.objects.filter(photo_report=photo_report)
                paste_watermarks(photos, photo_report.place)

                sequence_photos = []
                for photo in photos:
                    sequence_photos.append(photo.id)

                file_json = f'{ BASE_DIR }/media/sequence_photos/{ pr_id }.json'
                if os.path.exists(file_json):
                    sequence_photos_json = []
                    with open(file_json, 'r') as file_object:
                        sequence_photos_json = json.load(file_object)

                    if len(sequence_photos) > len(sequence_photos_json):
                        for photo_id in sequence_photos_json:
                            sequence_photos.remove(photo_id)

                        for photo_id in sequence_photos:
                            sequence_photos_json.append(photo_id)

                        with open(file_json, 'w') as file_object:
                            json.dump(sequence_photos_json, file_object)
                else:
                    with open(file_json, 'w') as file_object:
                        json.dump(sequence_photos, file_object)

                zip_create(pr_id)
                return redirect('photographer_dashboard:photo-reports')
            else:
                context['photo_report_form'] = photo_report_form
                context['photos_form'] = photos_form
                context['message'] = 'Error!'
                return render(request, 'photographer_dashboard/edit_photo_report.html', context)
        else:
            photo_report_form = PhotoReportForm(request, instance=photo_report)

            photos = []
            file_json = f'{ BASE_DIR }/media/sequence_photos/{ pr_id }.json'
            if os.path.exists(file_json):
                sequence_photos = []
                with open(file_json, 'r') as file_object:
                    sequence_photos = json.load(file_object)

                for photo_id in sequence_photos:
                    photo = get_object_or_404(Photo, id=photo_id)
                    photos.append(photo)
            else:
                photos = Photo.objects.filter(photo_report=photo_report)

            photos_form = PhotosForm()

            context['photo_report_form'] = photo_report_form
            context['photos'] = photos
            context['photos_form'] = photos_form
            return render(request, 'photographer_dashboard/edit_photo_report.html', context)
    else:
        raise PermissionDenied


@login_required
def delete_photo_report(request, pr_id):
    """ delete photo report """
    if user_access(request)['user_is_photographer']:
        photo_report = get_object_or_404(PhotoReport, id=pr_id)

        file_zip = f'{ BASE_DIR }/media/archives/{ photo_report.id }.zip'
        if os.path.exists(file_zip):
            os.remove(file_zip)

        file_json = f'{ BASE_DIR }/media/sequence_photos/{ photo_report.id }.json'
        if os.path.exists(file_json):
            os.remove(file_json)

        photo_report.delete()
        return redirect('photographer_dashboard:photo-reports')
    else:
        raise PermissionDenied


@login_required
def video_reports(request):
    """ video reports """
    if user_access(request)['user_is_photographer']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        video_reports = VideoReport.objects.filter(region=region)

        paginator = Paginator(video_reports, 10)
        page_number = request.GET.get('page', 1)
        video_reports_page = paginator.get_page(page_number)

        context = {
            'video_reports_page': video_reports_page,
        }
        return render(request, 'photographer_dashboard/video_reports.html', context)
    else:
        raise PermissionDenied


@login_required
def add_video_report(request):
    """ add video report """
    if user_access(request)['user_is_photographer']:
        if request.method == 'POST':
            video_report_form = VideoReportForm(request, request.POST, request.FILES)
            if video_report_form.is_valid():
                video_report_cd = video_report_form.cleaned_data
                video_report = video_report_form.save(commit=False)
                video_report.region = get_object_or_404(
                    Region, slug=request.session['user_region'])
                video_report.slug = slugify(unidecode(video_report_cd['title']))

                try:
                    video_report.save()
                except IntegrityError:
                    context = {
                        'video_report_form': video_report_form,
                        'message': 'Error!',
                    }
                    return render(request, 'photographer_dashboard/add_video_report.html', context)

                return redirect('photographer_dashboard:video-reports')
            else:
                context = {
                    'video_report_form': video_report_form,
                    'message': 'Error!',
                }
                return render(request, 'photographer_dashboard/add_video_report.html', context)
        else:
            video_report_form = VideoReportForm(
                request,
                initial={
                    'author': request.user.id,
                })
            context = {
                'video_report_form': video_report_form,
            }
            return render(request, 'photographer_dashboard/add_video_report.html', context)
    else:
        raise PermissionDenied


@login_required
def edit_video_report(request, video_report_id):
    """ edit video report """
    if user_access(request)['user_is_photographer']:
        video_report = get_object_or_404(VideoReport, id=video_report_id)

        context = {
            'video_report_id': video_report_id,
        }

        if request.method == 'POST':
            video_report_form = VideoReportForm(
                request, request.POST, request.FILES, instance=video_report)
            if video_report_form.is_valid():
                video_report_cd = video_report_form.cleaned_data
                video_report = video_report_form.save(commit=False)
                video_report.slug = slugify(unidecode(video_report_cd['title']))

                try:
                    video_report.save()
                except IntegrityError:
                    context['video_report_form'] = video_report_form
                    context['message'] = 'Error!'
                    return render(request, 'photographer_dashboard/edit_video_report.html', context)

                return redirect('photographer_dashboard:video-reports')
            else:
                context['video_report_form'] = video_report_form
                context['message'] = 'Error!'
                return render(request, 'photographer_dashboard/edit_video_report.html', context)
        else:
            video_report_form = VideoReportForm(request, instance=video_report)
            context['video_report_form'] = video_report_form
            return render(request, 'photographer_dashboard/edit_video_report.html', context)
    else:
        raise PermissionDenied


@login_required
def delete_video_report(request, video_report_id):
    """ delete video report """
    if user_access(request)['user_is_photographer']:
        video_report = get_object_or_404(VideoReport, id=video_report_id)
        video_report.delete()
        return redirect('photographer_dashboard:video-reports')
    else:
        raise PermissionDenied
