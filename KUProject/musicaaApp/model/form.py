from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .song import Song

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
    mood = models.CharField(max_length=20, choices=Mood.choices, blank=True, null=True)
    genre = models.CharField(max_length=20, choices=Genre.choices, blank=True, null=True)
    occasion = models.CharField(max_length=20, choices=Occasion.choices, blank=True, null=True)
    prompt = models.TextField(blank=True, null=True)
    singerIsMale = models.BooleanField()
    lengthInSeconds = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
    song = models.OneToOneField(Song, on_delete=models.SET_NULL, null=True, blank=True, related_name='form')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']