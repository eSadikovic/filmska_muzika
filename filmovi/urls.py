from django.conf.urls import url
from . import views

app_name = 'filmovi'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<film_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_film/$', views.create_film, name='create_film'),
    url(r'^(?P<film_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<film_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<film_id>[0-9]+)/favoritefilm/$', views.favoritefilm, name='favoritefilm'),
    url(r'^(?P<film_id>[0-9]+)/delete_film/$', views.delete_film, name='delete_film'),
]
