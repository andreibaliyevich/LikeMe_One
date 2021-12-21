from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main_app.models import Region
from places.models import Place
from .forms import VideoReportsCreateFilter
from .models import VideoReport, VideoLike


def video_reports_list(request):
    """ video reports list """
    region = get_object_or_404(Region, slug=request.session['user_region'])
    video_reports_filter = VideoReportsCreateFilter(request, request.GET or None)

    if request.method == 'GET' and video_reports_filter.is_valid():
        video_reports_filter_cd = video_reports_filter.cleaned_data
        place_id = int(video_reports_filter_cd['place'])
        place = get_object_or_404(Place, id=place_id)

        video_reports = VideoReport.objects.filter(place=place)
    else:
        video_reports = VideoReport.objects.filter(region=region)

    video_reports_tuples = []
    for video_report in video_reports:
        video_report_likes_count = VideoLike.objects.filter(
            video_report=video_report, is_like=True).count()
        video_reports_tuples.append((video_report, video_report_likes_count))

    paginator = Paginator(video_reports_tuples, 9)
    page_number = request.GET.get('page', 1)
    video_reports_page = paginator.get_page(page_number)

    context = {
        'video_reports_page': video_reports_page,
        'video_reports_filter': video_reports_filter,
    }
    return render(request, 'video_reports/list.html', context)


def video_report_detail(request, vr_id, vr_slug):
    """ video report detail """
    video_report = get_object_or_404(VideoReport, id=vr_id, slug=vr_slug)
    likes_count = VideoLike.objects.filter(
        video_report=video_report, is_like=True).count()

    try:
        user = User.objects.get(id=request.user.id)
        video_report_like = VideoLike.objects.get(
            user=user, video_report=video_report)
        user_is_liked = video_report_like.is_like
    except:
        user_is_liked = False

    video_report.num_views += 1
    video_report.save()

    context = {
        'title': video_report.title,
        'video_report': video_report,
        'likes_count': likes_count,
        'user_is_liked': user_is_liked,
    }
    return render(request, 'video_reports/detail.html', context)


@require_POST
def video_report_like(request):
    """ video report like """
    video_report = get_object_or_404(VideoReport, id=request.POST.get('vr_id'))
    user = get_object_or_404(User, id=request.user.id)

    try:
        add_video_report_like = VideoLike.objects.get(
            user=user, video_report=video_report)
        if add_video_report_like.is_like:
            add_video_report_like.is_like = False
        else:
            add_video_report_like.is_like = True
    except:
        add_video_report_like = VideoLike()
        add_video_report_like.user = user
        add_video_report_like.video_report = video_report

    add_video_report_like.save()

    data = {
        'likes_count': VideoLike.objects.filter(
            video_report=video_report, is_like=True).count()
    }
    return JsonResponse(data)
