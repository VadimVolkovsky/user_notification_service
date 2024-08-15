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
    pass


class Notification(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=NotificationType.choices)
    channel = models.CharField(max_length=255, choices=Chanel.choices)
    user = models.CharField(max_length=255, null=True, blank=True)
    user_group = models.CharField(max_length=255, null=True, blank=True)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    context = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} | {self.type}'
