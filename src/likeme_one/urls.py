"""likeme_one URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main_app.urls', namespace='main_app')),
    path('announcements/', include('announcements.urls', namespace='announcements')),
    path('photoreports/', include('photo_reports.urls', namespace='photo_reports')),
    path('videoreports/', include('video_reports.urls', namespace='video_reports')),
    path('places/', include('places.urls', namespace='places')),
    path('news/', include('news.urls', namespace='news')),
    path('admin-dashboard/', include('admin_dashboard.urls', namespace='admin_dashboard')),
    path('photographer-dashboard/', include('photographer_dashboard.urls', namespace='photographer_dashboard')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('tinymce/', include('tinymce.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'main_app.views.error_400'
handler403 = 'main_app.views.error_403'
handler404 = 'main_app.views.error_404'
handler500 = 'main_app.views.error_500'
