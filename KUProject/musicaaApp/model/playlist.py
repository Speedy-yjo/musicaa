from django.db import models
from django.core.exceptions import ValidationError

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='playlists')
    songs = models.ManyToManyField('Song', related_name='playlists', blank=True)

    def clean(self):
        if self.user.playlists.exclude(pk=self.pk).count() >= 100:
            raise ValidationError("One user can have at most 100 playlists.")
        if self.pk:
            if self.songs.count() > 100:
                raise ValidationError("A playlist can contain at most 100 songs.")

    def __str__(self):
        return self.name
