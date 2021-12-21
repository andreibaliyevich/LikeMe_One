from django.urls import path
from . import views


app_name = 'photographer_dashboard'
urlpatterns = [
    path('', views.photographer_dashboard, name='photographer-dashboard'),
    path('photo-reports/', views.photo_reports, name='photo-reports'),
    path('photo-reports/new/add/', views.add_photo_report, name='add-photo-report'),
    path('photo-reports/new-add-to-place/<int:place_id>/', views.add_photo_report_to_place, name='add-photo-report-to-place'),
    path('photo-reports/edit/<int:pr_id>/', views.edit_photo_report, name='edit-photo-report'),
    path('photo-reports/photo-upload/<int:pr_id>/', views.photo_upload, name='photo-upload'),
    path('photo-reports/photo-available/', views.photo_available, name='photo-available'),
    path('photo-reports/photo-cover/', views.photo_cover, name='photo-cover'),
    path('photo-reports/shuffle-photos/', views.shuffle_photos, name='shuffle-photos'),
    path('photo-reports/delete/<int:pr_id>/', views.delete_photo_report, name='delete-photo-report'),
    
    path('video-reports/', views.video_reports, name='video-reports'),
    path('video-reports/new/add/', views.add_video_report, name='add-video-report'),
    path('video-reports/edit/<int:video_report_id>/', views.edit_video_report, name='edit-video-report'),
    path('video-reports/delete/<int:video_report_id>/', views.delete_video_report, name='delete-video-report'),
]
