import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from likeme_one.settings import SITE_URL_ADDRESS
from main_app.models import Region
from .models import News


def news_list(request):
    """ news list """
    region = get_object_or_404(Region, slug=request.session['user_region'])
    news = News.objects.filter(region=region)

    paginator = Paginator(news, 9)
    page_number = request.GET.get('page', 1)
    news_page = paginator.get_page(page_number)
    
    context = {
        'news_page': news_page,
    }
    return render(request, 'news/list.html', context)


def news_list_by_author(request, author_id):
    """ news list by author """
    author = get_object_or_404(User, id=author_id)
    news = News.objects.filter(author=author)

    paginator = Paginator(news, 9)
    page_number = request.GET.get('page', 1)
    news_page = paginator.get_page(page_number)

    context = {
        'news_page': news_page,
    }
    return render(request, 'news/list.html', context)


def news_list_by_tag(request, news_tag):
    """ news list by tag """
    news = News.objects.filter(tags__name__in=[news_tag])

    paginator = Paginator(news, 9)
    page_number = request.GET.get('page', 1)
    news_page = paginator.get_page(page_number)

    context = {
        'news_page': news_page,
    }
    return render(request, 'news/list.html', context)


def news_detail(request, news_id, news_slug):
    """ news detail """
    one_news = get_object_or_404(News, id=news_id)    
    tags = one_news.tags.all()

    one_news.num_views += 1
    one_news.save()

    region = get_object_or_404(Region, slug=request.session['user_region'])
    news_more = News.objects.filter(region=region)
    news_more = news_more.exclude(id=news_id)
    news_more = news_more[:3]

    context = {
        'site_url_address': SITE_URL_ADDRESS,
        'one_news': one_news,
        'tags': tags,
        'news_more': news_more,
    }
    return render(request, 'news/detail.html', context)
