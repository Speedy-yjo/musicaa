from django.db import models
from django.core.exceptions import ValidationError

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Song(models.Model):
    class Status(models.TextChoices):
        GENERATING = 'generating', 'Generating'
        READY = 'ready', 'Ready'
        ERROR = 'error', 'Error'

    name = models.CharField(max_length=255)
    lengthInSeconds = models.PositiveIntegerField() 
    track = models.FileField(upload_to='songs/')
    status = models.CharField(max_length=20, choices=Status.choices)
    dateOfCreation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-dateOfCreation']


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


class Form(models.Model):
    class Mood(models.TextChoices):
        HAPPY = 'happy', 'Happy'
        SAD = 'sad', 'Sad'
        MOTIVATION = 'motivation', 'Motivation'
        CALM = 'calm', 'Calm'
        ROMANTIC = 'romantic', 'Romantic'

    class Genre(models.TextChoices):
        POP = 'pop', 'Pop'
        ROCK = 'rock', 'Rock'
        CLASSICAL = 'classical', 'Classical'
        LATIN = 'latin', 'Latin'
        ALTERNATIVE = 'alternative', 'Alternative'
        INDIE = 'indie', 'Indie'

    class Occasion(models.TextChoices):
        WEDDING = 'wedding', 'Wedding'
        PARTY = 'party', 'Party'
        BIRTHDAY = 'birthday', 'Birthday'

    name = models.CharField(max_length=255)
    mood = models.CharField(max_length=20, choices=Mood.choices)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    occasion = models.CharField(max_length=20, choices=Occasion.choices)
    prompt = models.TextField()
    singerIsMale = models.BooleanField()
    lengthInSeconds = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
    song = models.OneToOneField(Song, on_delete=models.SET_NULL, null=True, blank=True, related_name='form')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']