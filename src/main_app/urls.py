from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.urls import path, reverse_lazy
from . import views


app_name = 'main_app'
urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/login/',
        LoginView.as_view(template_name='main_app/users/login.html'),
        name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('accounts/password/change/',
        PasswordChangeView.as_view(
            template_name='main_app/users/password-change.html',
            success_url=reverse_lazy('main_app:password-change-done')),
        name='password-change'),
    path('accounts/password/change/done/',
        PasswordChangeDoneView.as_view(
            template_name='main_app/users/password-change-done.html'),
        name='password-change-done'),

    path('search/', views.search, name='search'),
    path('photographer-order/', views.photographer_order, name='photographer-order'),

    path('set/region/<str:region_slug>/', views.set_region, name='set-region'),
    path('set/language/<str:language_code>/', views.set_language, name='set-language'),

    path('about/', views.about, name='about'),
    path('policy/', views.policy, name='policy'),
    path('vacancy/', views.vacancy, name='vacancy'),
]
