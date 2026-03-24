from django.contrib import admin
from .model.user import User
from .model.song import Song
from .model.playlist import Playlist
from .model.form import Form

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'dateOfCreation')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    filter_horizontal = ('songs',)

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'mood', 'genre', 'occasion', 'created_at')
    list_filter = ('mood', 'genre', 'occasion')