from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.news_list, name='news-list'),

    path('author/<int:author_id>/',
        views.news_list_by_author,
        name='news-list-by-author'),

    path('tag/<str:news_tag>/',
        views.news_list_by_tag,
        name='news-list-by-tag'),

    path('<int:news_id>/<str:news_slug>/',
        views.news_detail,
        name='news-detail'),
]
