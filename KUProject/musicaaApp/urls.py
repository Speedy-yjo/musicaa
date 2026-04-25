from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_view, name='library'),
    path('generate/', views.generate_view, name='generate'),
    path('song/<int:song_id>/delete/', views.delete_song_view, name='delete_song'),
    path('song/<int:song_id>/download/', views.download_song_view, name='download_song'),
    path('share/<uuid:share_token>/', views.shared_song_view, name='shared_song'),
    path('share/<uuid:share_token>/download/', views.download_shared_song_view, name='download_shared_song'),
    path('playlists/', views.playlists_view, name='playlists'),
    path('playlists/<int:playlist_id>/', views.playlist_detail_view, name='playlist_detail'),
    path('playlists/add/<int:song_id>/', views.add_to_playlist_action, name='add_to_playlist'),
    path('playlists/remove/<int:playlist_id>/<int:song_id>/', views.remove_from_playlist_action, name='remove_from_playlist'),
    path('api/poll-status/', views.poll_generation_status, name='poll_status'),
]
