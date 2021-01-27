from django.urls import path
from .views import *

index = IndexView.as_view()
searched_movies = SearchedMovieView.as_view()
movie_detail = StoryMovieView.as_view()
notices = NoticeListView.as_view()
notice_detail = NoticeDetailView.as_view()
movie_detail_cover = StoryMovieCoverView.as_view()
movie_detail_black = StoryMovieBlackView.as_view()
movie_detail_white = StoryMovieWhiteView.as_view()
contact_us = ContactUsView.as_view()


urlpatterns = [
    path('', index, name='index'),
    path('searched_movies', searched_movies, name='searched_movies'),
    path('searched_movies/<str:pk>', movie_detail, name='movie_detail'),
    path('searched_movies/<str:pk>/cover', movie_detail_cover, name='movie_detail_cover'),
    path('searched_movies/<str:pk>/black', movie_detail_black, name='movie_detail_black'),
    path('searched_movies/<str:pk>/white', movie_detail_white, name='movie_detail_white'),
    path('notices', notices, name='notices'),
    path('notices/<str:pk>', notice_detail, name='notice_detail'),
    path('contact_us', contact_us, name='contact_us')
]