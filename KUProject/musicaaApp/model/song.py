from django.db import models
from django.core.exceptions import ValidationError
from .user import User

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
