from django.urls import path
from . import views


app_name = 'announcements'
urlpatterns = [
    path('', views.announcements_list, name='announcements-list'),
]
