from django.urls import path
from .views import *

index = IndexView.as_view()
searched_movies = SearchedMovieView.as_view()
movie_detail = StoryMovieView.as_view()
notices = NoticeListView.as_view()
notice_detail = NoticeDetailView.as_view()


urlpatterns = [
    path('', index, name='index'),
    path('searched_movies', searched_movies, name='searched_movies'),
    path('searched_movies/<str:pk>', movie_detail, name='movie_detail'),
    path('notices', notices, name='notices'),
    path('notices/<str:pk>', notice_detail, name='notice_detail')
]