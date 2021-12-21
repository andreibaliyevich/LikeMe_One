from django.urls import path
from . import views


app_name = 'admin_dashboard'
urlpatterns = [
    path('', views.admin_dashboard, name='admin-dashboard'),
    path('admins/', views.admins, name='admins'),
    path('admins/search/', views.admins_search, name='admins-search'),
    path('admins/add/<int:add_admin_id>/', views.add_admin, name='add-admin'),
    path('admins/del/<int:del_admin_id>/', views.del_admin, name='del-admin'),
    
    path('photographers/', views.photographers, name='photographers'),
    path('photographers/search/', views.photographers_search, name='photographers-search'),
    path('photographers/add/<int:add_photographer_id>/', views.add_photographer, name='add-photographer'),
    path('photographers/del/<int:del_photographer_id>/', views.del_photographer, name='del-photographer'),

    path('payments/', views.payments, name='payments'),
    
    path('banners/', views.banners, name='banners'),
    path('banners/add/', views.add_banner, name='add-banner'),
    path('banners/edit/<int:banner_id>/', views.edit_banner, name='edit-banner'),
    path('banners/delete/<int:banner_id>/', views.delete_banner, name='delete-banner'),
    
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/add/', views.add_announcement, name='add-announcement'),
    path('announcements/edit/<int:announcement_id>/', views.edit_announcement, name='edit-announcement'),
    path('announcements/delete/<int:announcement_id>/', views.delete_announcement, name='delete-announcement'),
    
    path('places/', views.places, name='places'),
    path('places/search/', views.places_search, name='places-search'),
    path('places/add/', views.add_place, name='add-place'),
    path('places/edit/<int:place_id>/', views.edit_place, name='edit-place'),
    path('places/delete/<int:place_id>/', views.delete_place, name='delete-place'),

    path('news/', views.news, name='news'),
    path('news/add/', views.add_news, name='add-news'),
    path('news/image-upload/', views.image_upload, name='image-upload'),
    path('news/edit/<int:news_id>/', views.edit_news, name='edit-news'),
    path('news/delete/<int:news_id>/', views.delete_news, name='delete-news'),
    
    path('photographer-orders/', views.photographer_orders, name='photographer-orders'),
]
