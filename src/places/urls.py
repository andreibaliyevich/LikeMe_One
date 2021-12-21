from django.urls import path
from . import views


app_name = 'places'
urlpatterns = [
    path('', views.places_list, name='places-list'),
    path('<int:place_id>/<str:place_slug>/',
        views.place_detail,
        name='place-detail'),
]
