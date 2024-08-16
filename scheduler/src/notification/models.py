import uuid

from django.db import models


class Chanel(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push'


class NotificationType(models.TextChoices):
    SIGN_UP = 'sign_up', 'Sign up'
    REVIEW_LIKE = 'review_like', 'Review like'
    NEW_FILM = 'new_film', 'New film'
    NEW_EPISODE = 'new_episode', 'New episode'
    BOOKMARKS = 'bookmarks', 'Bookmarks'
    INFO = 'info', 'Info'


class NotificationTemplate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    template = models.TextField()

    def __str__(self):
        return f'{self.title}'


class Status(models.TextChoices):
    INITIAL = 'initial', 'Initial'
    SENT = 'sent', 'Sent'
    ERROR = 'error', 'Error'


class Notification(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=NotificationType.choices)
    channel = models.CharField(max_length=255, choices=Chanel.choices)
    recipients = models.JSONField(null=True, blank=True)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    context = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIAL.name)

    def __str__(self):
        return f'{self.title} | {self.type}'


class UserSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allowed_email = models.BooleanField(default=True)
    allowed_push = models.BooleanField(default=True)
    time_zone = models.CharField(max_length=10)
