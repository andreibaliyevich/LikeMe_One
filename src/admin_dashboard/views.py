from unidecode import unidecode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from main_app.models import Region, UserAccess, Banner, PhotographerOrder
from main_app.context_processors import user_access
from photo_reports.models import PhotoReport
from video_reports.models import VideoReport
from announcements.models import Announcement
from places.models import Place
from news.models import News, Image
from .forms import DateForm, BannerForm, AnnouncementForm, PlaceForm, NewsForm
from .utilities import user_is_superadmin


@login_required
def admin_dashboard(request):
    """ admin dashboard """
    return redirect('admin_dashboard:admins')


@login_required
def admins(request):
    """ Admins """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        admins = User.objects.filter(
            user_access__region=region, user_access__is_admin=True)

        context = {
            'admins': admins,
        }
        return render(request, 'admin_dashboard/admins.html', context)
    else:
        raise PermissionDenied


@login_required
def admins_search(request):
    """ admins search """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        admins = User.objects.filter(
            user_access__region=region, user_access__is_admin=True)
        all_users = User.objects.all()

        users = []
        for user in all_users:
            if user not in admins:
                users.append(user)

        users_found = []
        input_search = request.GET.get('search', '')
        if input_search:
            input_search = input_search.lower()

            for user in users:
                username = user.username.lower()
                first_name = user.first_name.lower()
                last_name = user.last_name.lower()

                if input_search in username:
                    users_found.append(user)
                elif input_search in first_name:
                    users_found.append(user)
                elif input_search in last_name:
                    users_found.append(user)

        context = {
            'admins': admins,
            'users_found': users_found,
        }
        return render(request, 'admin_dashboard/admins.html', context)
    else:
        raise PermissionDenied


@login_required
def add_admin(request, add_admin_id):
    """ add admin """
    if user_access(request)['user_is_admin']:
        add_admin = get_object_or_404(User, id=add_admin_id)
        region = get_object_or_404(
                Region, slug=request.session['user_region'])
        try:
            add_admin_access = UserAccess.objects.get(
                user=add_admin, region=region)
        except:
            add_admin_access = UserAccess()
            add_admin_access.user = add_admin
            add_admin_access.region = region

        add_admin_access.is_admin = True
        add_admin_access.save()

        return redirect('admin_dashboard:admins')
    else:
        raise PermissionDenied


@login_required
def del_admin(request, del_admin_id):
    """ del admin """
    if user_access(request)['user_is_admin']:
        admin = get_object_or_404(User, id=request.user.id)
        del_admin = get_object_or_404(User, id=del_admin_id)

        if user_is_superadmin(admin) or not user_is_superadmin(del_admin):
            region = get_object_or_404(
                Region, slug=request.session['user_region'])
            del_admin_access = get_object_or_404(
                UserAccess, user=del_admin, region=region)
            del_admin_access.is_admin = False
            del_admin_access.save()

        return redirect('admin_dashboard:admins')
    else:
        raise PermissionDenied


@login_required
def photographers(request):
    """ Photographers """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        photographers = User.objects.filter(
            user_access__region=region, user_access__is_photographer=True)

        context = {
            'photographers': photographers,
        }
        return render(request, 'admin_dashboard/photographers.html', context)
    else:
        raise PermissionDenied


@login_required
def photographers_search(request):
    """ photographers search """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        photographers = User.objects.filter(
            user_access__region=region, user_access__is_photographer=True)
        all_users = User.objects.all()

        users = []
        for user in all_users:
            if user not in photographers:
                users.append(user)

        users_found = []
        input_search = request.GET.get('search', '')
        if input_search:
            input_search = input_search.lower()

            for user in users:
                username = user.username.lower()
                first_name = user.first_name.lower()
                last_name = user.last_name.lower()

                if input_search in username:
                    users_found.append(user)
                elif input_search in first_name:
                    users_found.append(user)
                elif input_search in last_name:
                    users_found.append(user)

        context = {
            'photographers': photographers,
            'users_found': users_found,
        }
        return render(request, 'admin_dashboard/photographers.html', context)
    else:
        raise PermissionDenied


@login_required
def add_photographer(request, add_photographer_id):
    """ add photographer """
    if user_access(request)['user_is_admin']:
        add_photographer = get_object_or_404(User, id=add_photographer_id)
        region = get_object_or_404(
                Region, slug=request.session['user_region'])
        try:
            add_photographer_access = UserAccess.objects.get(
                user=add_photographer, region=region)
        except:
            add_photographer_access = UserAccess()
            add_photographer_access.user = add_photographer
            add_photographer_access.region = region

        add_photographer_access.is_photographer = True
        add_photographer_access.save()

        return redirect('admin_dashboard:photographers')
    else:
        raise PermissionDenied


@login_required
def del_photographer(request, del_photographer_id):
    """ del photographer """
    if user_access(request)['user_is_admin']:
        admin = get_object_or_404(User, id=request.user.id)
        del_photographer = get_object_or_404(User, id=del_photographer_id)

        if user_is_superadmin(admin) or not user_is_superadmin(del_photographer):
            region = get_object_or_404(
                Region, slug=request.session['user_region'])
            del_photographer_access = get_object_or_404(
                UserAccess, user=del_photographer, region=region)
            del_photographer_access.is_photographer = False
            del_photographer_access.save()

        return redirect('admin_dashboard:photographers')
    else:
        raise PermissionDenied


@login_required
def payments(request):
    """ Payments """
    if user_access(request)['user_is_admin']:
        if request.method == 'POST':
            date_form = DateForm(request, request.POST)
            if date_form.is_valid():
                date_form_cd = date_form.cleaned_data
                date = date_form_cd['date'].split('-')
                date_year = int(date[0])
                date_month = int(date[1])
        else:
            date_form = DateForm(request)
            date_year = int(timezone.now().year)
            date_month = int(timezone.now().month)

        region = get_object_or_404(Region, slug=request.session['user_region'])
        photo_reports = PhotoReport.objects.filter(
            region=region, date__year=date_year, date__month=date_month)
        video_reports = VideoReport.objects.filter(
            region=region, date__year=date_year, date__month=date_month)

        authors_photo_reports = User.objects.filter(
            photoreports__region=region,
            photoreports__date__year=date_year,
            photoreports__date__month=date_month).distinct()
        authors_video_reports = User.objects.filter(
            videoreports__region=region,
            videoreports__date__year=date_year,
            videoreports__date__month=date_month).distinct()

        authors_photo_dicts = []
        summary_photo = {'count': 0, 'invoice': 0, 'tax': 0}
        for author_photo_reports in authors_photo_reports:
            author_photo_dict = {}

            if author_photo_reports.get_full_name():
                author_photo_dict['author'] = author_photo_reports.get_full_name()
            else:
                author_photo_dict['author'] = author_photo_reports.get_username()

            author_photo_dict['reports'] = photo_reports.filter(
                author=author_photo_reports)

            count, invoice, tax = 0, 0, 0
            for photo_report in author_photo_dict['reports']:
                invoice += photo_report.pay_to_photographer
                tax += photo_report.pay_to_portal
                count += 1
            author_photo_dict['summary'] = (count, invoice, tax)
            summary_photo['count'] += count
            summary_photo['invoice'] += invoice
            summary_photo['tax'] += tax

            authors_photo_dicts.append(author_photo_dict)

        authors_video_dicts = []
        summary_video = {'count': 0, 'invoice': 0, 'tax': 0}
        for author_video_reports in authors_video_reports:
            author_video_dict = {}

            if author_video_reports.get_full_name():
                author_video_dict['author'] = author_video_reports.get_full_name()
            else:
                author_video_dict['author'] = author_video_reports.get_username()

            author_video_dict['reports'] = video_reports.filter(
                author=author_video_reports)

            count, invoice, tax = 0, 0, 0
            for video_report in author_video_dict['reports']:
                invoice += video_report.pay_to_photographer
                tax += video_report.pay_to_portal
                count += 1
            author_video_dict['summary'] = (count, invoice, tax)
            summary_video['count'] += count
            summary_video['invoice'] += invoice
            summary_video['tax'] += tax

            authors_video_dicts.append(author_video_dict)

        summary = {
            'count': summary_photo['count'] + summary_video['count'],
            'invoice': summary_photo['invoice'] + summary_video['invoice'],
            'tax': summary_photo['tax'] + summary_video['tax'],
        }

        context = {
            'date_form': date_form,
            'authors_photo_dicts': authors_photo_dicts,
            'authors_video_dicts': authors_video_dicts,
            'summary_photo': summary_photo,
            'summary_video': summary_video,
            'summary': summary,
        }
        return render(request, 'admin_dashboard/payments.html', context)
    else:
        raise PermissionDenied


@login_required
def banners(request):
    """ Banners """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        banners = Banner.objects.filter(region=region)

        context = {
            'banners': banners,
        }
        return render(request, 'admin_dashboard/banners.html', context)
    else:
        raise PermissionDenied


@login_required
def add_banner(request):
    """ add banner """
    if user_access(request)['user_is_admin']:
        if request.method == 'POST':
            banner_form = BannerForm(request.POST, request.FILES)
            if banner_form.is_valid():
                banner = banner_form.save(commit=False)
                banner.region = get_object_or_404(
                    Region, slug=request.session['user_region'])

                try:
                    banner.save()
                except IntegrityError:
                    context = {
                        'banner_form': banner_form,
                        'message': 'Error!',
                    }
                    return render(request, 'admin_dashboard/add/banner.html', context)

                return redirect('admin_dashboard:banners')
            else:
                context = {
                    'banner_form': banner_form,
                    'message': 'Error!',
                }
                return render(request, 'admin_dashboard/add/banner.html', context)
        else:
            banner_form = BannerForm()
            context = {
                'banner_form': banner_form,
            }
            return render(request, 'admin_dashboard/add/banner.html', context)
    else:
        raise PermissionDenied


@login_required
def edit_banner(request, banner_id):
    """ edit banner """
    if user_access(request)['user_is_admin']:
        banner = get_object_or_404(Banner, id=banner_id)

        context = {
            'banner_id': banner_id,
        }

        if request.method == 'POST':
            banner_form = BannerForm(request.POST, request.FILES, instance=banner)
            if banner_form.is_valid():
                banner_form.save()
                return redirect('admin_dashboard:banners')
            else:
                context['banner_form'] = banner_form
                context['message'] = 'Error!'
                return render(request, 'admin_dashboard/edit/banner.html', context)
        else:
            banner_form = BannerForm(instance=banner)
            context['banner_form'] = banner_form
            return render(request, 'admin_dashboard/edit/banner.html', context)
    else:
        raise PermissionDenied


@login_required
def delete_banner(request, banner_id):
    """ delete banner """
    if user_access(request)['user_is_admin']:
        banner = get_object_or_404(Banner, id=banner_id)
        banner.delete()
        return redirect('admin_dashboard:banners')
    else:
        raise PermissionDenied


@login_required
def announcements(request):
    """ Announcements """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        announcements = Announcement.objects.filter(region=region)

        paginator = Paginator(announcements, 10)
        page_number = request.GET.get('page', 1)
        announcements_page = paginator.get_page(page_number)

        context = {
            'announcements_page': announcements_page,
        }
        return render(request, 'admin_dashboard/announcements.html', context)
    else:
        raise PermissionDenied


@login_required
def add_announcement(request):
    """ add announcement """
    if user_access(request)['user_is_admin']:
        if request.method == 'POST':
            announcement_form = AnnouncementForm(request, request.POST, request.FILES)
            if announcement_form.is_valid():
                announcement = announcement_form.save(commit=False)
                announcement.region = get_object_or_404(
                    Region, slug=request.session['user_region'])

                try:
                    announcement.save()
                except IntegrityError:
                    context = {
                        'announcement_form': announcement_form,
                        'message': 'Error!',
                    }
                    return render(request, 'admin_dashboard/add/announcement.html', context)

                return redirect('admin_dashboard:announcements')
            else:
                context = {
                    'announcement_form': announcement_form,
                    'message': 'Error!',
                }
                return render(request, 'admin_dashboard/add/announcement.html', context)
        else:
            announcement_form = AnnouncementForm(request)
            context = {
                'announcement_form': announcement_form,
            }
            return render(request, 'admin_dashboard/add/announcement.html', context)
    else:
        raise PermissionDenied


@login_required
def edit_announcement(request, announcement_id):
    """ edit announcement """
    if user_access(request)['user_is_admin']:
        announcement = get_object_or_404(Announcement, id=announcement_id)

        context = {
            'announcement_id': announcement_id,
        }

        if request.method == 'POST':
            announcement_form = AnnouncementForm(
                request, request.POST, request.FILES, instance=announcement)
            if announcement_form.is_valid():
                announcement_form.save()
                return redirect('admin_dashboard:announcements')
            else:
                context['announcement_form'] = announcement_form
                context['message'] = 'Error!'
                return render(request, 'admin_dashboard/edit/announcement.html', context)
        else:
            announcement_form = AnnouncementForm(request, instance=announcement)
            context['announcement_form'] = announcement_form
            return render(request, 'admin_dashboard/edit/announcement.html', context)
    else:
        raise PermissionDenied


@login_required
def delete_announcement(request, announcement_id):
    """ delete announcement """
    if user_access(request)['user_is_admin']:
        announcement = get_object_or_404(Announcement, id=announcement_id)
        announcement.delete()
        return redirect('admin_dashboard:announcements')
    else:
        raise PermissionDenied


@login_required
def places(request):
    """ Places """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        places = Place.objects.exclude(id=1).filter(region=region)

        paginator = Paginator(places, 10)
        page_number = request.GET.get('page', 1)
        places_page = paginator.get_page(page_number)

        context = {
            'places_page': places_page,
        }
        return render(request, 'admin_dashboard/places.html', context)
    else:
        raise PermissionDenied


@login_required
def places_search(request):
    """ places search """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        places = Place.objects.exclude(id=1).filter(region=region)

        places_found = []
        input_search = request.GET.get('search', '')
        if input_search:
            input_search = input_search.lower()

            for place in places:
                if input_search in place.name.lower():
                    places_found.append(place)

        paginator = Paginator(places_found, 10)
        page_number = request.GET.get('page', 1)
        places_page = paginator.get_page(page_number)

        context = {
            'places_page': places_page,
        }
        return render(request, 'admin_dashboard/places.html', context)
    else:
        raise PermissionDenied


@login_required
def add_place(request):
    """ add place """
    if user_access(request)['user_is_admin']:
        if request.method == 'POST':
            place_form = PlaceForm(request, request.POST, request.FILES)
            if place_form.is_valid():
                place_form_cd = place_form.cleaned_data
                place = place_form.save(commit=False)
                place.region = get_object_or_404(
                    Region, slug=request.session['user_region'])
                place.slug = slugify(unidecode(place_form_cd['name']))

                if place_form_cd['working_hours'] == "o'clock":
                    working_hours = f"{ place_form_cd['from_hour'] }:00 - { place_form_cd['to_hour'] }:00"
                    place.working_hours = working_hours
                elif place_form_cd['working_hours'] == '24/7':
                    place.working_hours = place_form_cd['working_hours']

                try:
                    place.save()
                except IntegrityError:
                    context = {
                        'place_form': place_form,
                        'message': 'Error!',
                    }
                    return render(request, 'admin_dashboard/add/place.html', context)

                return redirect('admin_dashboard:places')
            else:
                context = {
                    'place_form': place_form,
                    'message': 'Error!',
                }
                return render(request, 'admin_dashboard/add/place.html', context)
        else:
            place_form = PlaceForm(request)
            context = {
                'place_form': place_form,
            }
            return render(request, 'admin_dashboard/add/place.html', context)
    else:
        raise PermissionDenied


@login_required
def edit_place(request, place_id):
    """ edit place """
    if user_access(request)['user_is_admin']:
        place = get_object_or_404(Place, id=place_id)

        context = {
            'place_id': place_id,
        }

        if request.method == 'POST':
            place_form = PlaceForm(request, request.POST, request.FILES, instance=place)
            if place_form.is_valid():
                place_form_cd = place_form.cleaned_data
                place = place_form.save(commit=False)
                place.slug = slugify(unidecode(place_form_cd['name']))

                if place_form_cd['working_hours'] == "o'clock":
                    working_hours = f"{ place_form_cd['from_hour'] }:00 - { place_form_cd['to_hour'] }:00"
                    place.working_hours = working_hours
                elif place_form_cd['working_hours'] == '24/7':
                    place.working_hours = place_form_cd['working_hours']

                try:
                    place.save()
                except IntegrityError:
                    context['place_form'] = place_form
                    context['message'] = 'Error!'
                    return render(request, 'admin_dashboard/edit/place.html', context)

                return redirect('admin_dashboard:places')
            else:
                context['place_form'] = place_form
                context['message'] = 'Error!'
                return render(request, 'admin_dashboard/edit/place.html', context)
        else:
            if place.working_hours == '24/7':
                place_form = PlaceForm(
                    request,
                    instance=place,
                    initial={
                        'working_hours': '24/7',
                    })
            elif place.working_hours:
                working_hours_split = place.working_hours.split()
                place_form = PlaceForm(
                    request,
                    instance=place,
                    initial={
                        'working_hours': "o'clock",
                        'from_hour': working_hours_split[0].split(':')[0],
                        'to_hour': working_hours_split[2].split(':')[0],
                    })
            else:
                place_form = PlaceForm(request, instance=place)
            
            context['place_form'] = place_form
            return render(request, 'admin_dashboard/edit/place.html', context)
    else:
        raise PermissionDenied


@login_required
def delete_place(request, place_id):
    """ delete place """
    if user_access(request)['user_is_admin']:
        place = get_object_or_404(Place, id=place_id)
        place.delete()
        return redirect('admin_dashboard:places')
    else:
        raise PermissionDenied


@require_POST
@csrf_protect
def image_upload(request):
    """ image upload for news """
    if request.FILES:
        upload_image = Image()
        upload_image.image = request.FILES['file']
        upload_image.owner = request.user.id
        upload_image.save()

        data = { 'location': upload_image.image.url }
        return JsonResponse(data)
    else:
        return HttpResponse(_('Form not valid!'), status=400)


@login_required
def news(request):
    """ News """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        news = News.objects.filter(region=region)

        paginator = Paginator(news, 10)
        page_number = request.GET.get('page', 1)
        news_page = paginator.get_page(page_number)

        context = {
            'news_page': news_page,
        }
        return render(request, 'admin_dashboard/news.html', context)
    else:
        raise PermissionDenied


@login_required
def add_news(request):
    """ add news """
    if user_access(request)['user_is_admin']:
        if request.method == 'POST':
            news_form = NewsForm(request, request.POST, request.FILES)
            if news_form.is_valid():
                news_form_cd = news_form.cleaned_data
                one_news = news_form.save(commit=False)
                one_news.region = get_object_or_404(
                    Region, slug=request.session['user_region'])
                one_news.slug = slugify(unidecode(news_form_cd['title']))

                try:
                    one_news.save()
                    news_form.save_m2m()
                except IntegrityError:
                    context = {
                        'news_form': news_form,
                        'message': 'Error!',
                    }
                    return render(request, 'admin_dashboard/add/news.html', context)

                return redirect('admin_dashboard:news')
            else:
                context = {
                    'news_form': news_form,
                    'message': 'Error!',
                }
                return render(request, 'admin_dashboard/add/news.html', context)
        else:
            news_form = NewsForm(
                request,
                initial={
                    'author': request.user.id,
                })
            context = {
                'news_form': news_form,
            }
            return render(request, 'admin_dashboard/add/news.html', context)
    else:
        raise PermissionDenied


@login_required
def edit_news(request, news_id):
    """ edit news """
    if user_access(request)['user_is_admin']:
        one_news = get_object_or_404(News, id=news_id)

        context = {
            'news_id': news_id,
        }

        if request.method == 'POST':
            news_form = NewsForm(request, request.POST, request.FILES, instance=one_news)
            if news_form.is_valid():
                news_form_cd = news_form.cleaned_data
                one_news = news_form.save(commit=False)                
                one_news.slug = slugify(unidecode(news_form_cd['title']))

                try:
                    one_news.save()
                    news_form.save_m2m()
                except IntegrityError:
                    context['news_form'] = news_form
                    context['message'] = 'Error!'
                    return render(request, 'admin_dashboard/edit/news.html', context)

                return redirect('admin_dashboard:news')
            else:
                context['news_form'] = news_form
                context['message'] = 'Error!'
                return render(request, 'admin_dashboard/edit/news.html', context)
        else:
            news_form = NewsForm(request, instance=one_news)
            context['news_form'] = news_form
            return render(request, 'admin_dashboard/edit/news.html', context)
    else:
        raise PermissionDenied


@login_required
def delete_news(request, news_id):
    """ delete news """
    if user_access(request)['user_is_admin']:
        one_news = get_object_or_404(News, id=news_id)
        one_news.delete()
        return redirect('admin_dashboard:news')
    else:
        raise PermissionDenied


@login_required
def photographer_orders(request):
    """ Photographer Orders """
    if user_access(request)['user_is_admin']:
        region = get_object_or_404(Region, slug=request.session['user_region'])
        photographer_orders = PhotographerOrder.objects.filter(region=region)

        for order in photographer_orders.filter(viewed=False):
            order.viewed = True
            order.save()

        context = {
            'photographer_orders': photographer_orders,
        }
        return render(request, 'admin_dashboard/photographer-orders.html', context)
    else:
        raise PermissionDenied
