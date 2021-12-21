from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from main_app.models import Region
from photo_reports.models import PhotoReport, PhotoLike
from .forms import PlacesCreateFilter
from .models import District, Place


def places_list(request):
    """ places list """
    region = get_object_or_404(Region, slug=request.session['user_region'])
    places = Place.objects.filter(region=region, is_closed=False)
    places_filter = PlacesCreateFilter(request, request.GET or None)
    
    if request.method == 'GET' and places_filter.is_valid():
        places_filter_cd = places_filter.cleaned_data
        
        if places_filter_cd['type_place']:
            if places_filter_cd['type_place'] == 'bar':
                places = places.filter(bar=True)
            elif places_filter_cd['type_place'] == 'hookah':
                places = places.filter(hookah=True)
            elif places_filter_cd['type_place'] == 'restaurant':
                places = places.filter(restaurant=True)
            elif places_filter_cd['type_place'] == 'night_club':
                places = places.filter(night_club=True)
            elif places_filter_cd['type_place'] == 'karaoke':
                places = places.filter(karaoke=True)
            elif places_filter_cd['type_place'] == 'veranda':
                places = places.filter(veranda=True)
            elif places_filter_cd['type_place'] == 'strip_club':
                places = places.filter(strip_club=True)
            elif places_filter_cd['type_place'] == 'brewery':
                places = places.filter(brewery=True)
            elif places_filter_cd['type_place'] == 'bowling':
                places = places.filter(bowling=True)
            elif places_filter_cd['type_place'] == 'coffee_house':
                places = places.filter(coffee_house=True)
            elif places_filter_cd['type_place'] == 'educational_project':
                places = places.filter(educational_project=True)
            elif places_filter_cd['type_place'] == 'entertainment':
                places = places.filter(entertainment=True)
            elif places_filter_cd['type_place'] == 'health':
                places = places.filter(health=True)
            elif places_filter_cd['type_place'] == 'store':
                places = places.filter(store=True)
        
        if places_filter_cd['district_place']:
            district_id = int(places_filter_cd['district_place'])
            district = get_object_or_404(District, id=district_id)
            places = places.filter(district=district)
        
        if places_filter_cd['kitchen_place']:
            if places_filter_cd['kitchen_place'] == 'kitchen_european':
                places = places.filter(kitchen_european=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_american':
                places = places.filter(kitchen_american=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_italian':
                places = places.filter(kitchen_italian=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_author':
                places = places.filter(kitchen_author=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_ukrainian':
                places = places.filter(kitchen_ukrainian=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_belarusian':
                places = places.filter(kitchen_belarusian=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_russian':
                places = places.filter(kitchen_russian=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_armenian':
                places = places.filter(kitchen_armenian=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_azerbaijani':
                places = places.filter(kitchen_azerbaijani=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_georgian':
                places = places.filter(kitchen_georgian=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_spanish':
                places = places.filter(kitchen_spanish=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_mexican':
                places = places.filter(kitchen_mexican=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_japanese':
                places = places.filter(kitchen_japanese=True)
            elif places_filter_cd['kitchen_place'] == 'kitchen_indian':
                places = places.filter(kitchen_indian=True)

    paginator = Paginator(places, 9)
    page_number = request.GET.get('page', 1)
    places_page = paginator.get_page(page_number)

    context = {
        'places_page': places_page,
        'places_filter': places_filter,
    }

    return render(request, 'places/list.html', context)


def place_detail(request, place_id, place_slug):
    """ place detail """
    place = get_object_or_404(Place, id=place_id)
    
    photo_reports = PhotoReport.objects.filter(place=place, is_posted=True)
    photo_reports_tuples = []
    for photo_report in photo_reports:
        photo_report_likes_count = PhotoLike.objects.filter(
            photo__photo_report=photo_report, is_like=True).count()
        photo_reports_tuples.append((photo_report, photo_report_likes_count))

    context = {
        'place': place,
        'photo_reports_tuples': photo_reports_tuples,
    }

    return render(request, 'places/detail.html', context)
