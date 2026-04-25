import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Song(models.Model):
    class Status(models.TextChoices):
        GENERATING = 'generating', 'Generating'
        READY = 'ready', 'Ready'
        ERROR = 'error', 'Error'

    name = models.CharField(max_length=255)
    lengthInSeconds = models.PositiveIntegerField()
    track = models.FileField(upload_to='songs/', blank=True, null=True)
    audio_url = models.URLField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    task_id = models.CharField(max_length=255, blank=True, null=True)
    dateOfCreation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-dateOfCreation']
