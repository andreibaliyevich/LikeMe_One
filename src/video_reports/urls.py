from django.urls import path
from . import views


app_name = 'video_reports'
urlpatterns = [
    path('', views.video_reports_list, name='video-reports-list'),
    path('<int:vr_id>/<str:vr_slug>/',
        views.video_report_detail,
        name='video-report-detail'),
    path('video/like/', views.video_report_like, name='video-report-like'),
]
