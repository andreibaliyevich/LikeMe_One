from django.urls import path
from . import views


app_name = 'photo_reports'
urlpatterns = [
    path('', views.photo_reports_list, name='photo-reports-list'),
    path('<int:pr_id>/<str:pr_slug>/',
        views.photo_report_detail,
        name='photo-report-detail'),
    path('photo/view/', views.photo_view, name='photo-view'),
    path('photo/like/', views.photo_like, name='photo-like'),
    path('download-archive/<int:pr_id>/',
        views.download_archive,
        name='download-archive'),
]
