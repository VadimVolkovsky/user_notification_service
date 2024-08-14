from django.db import models


class Chanel(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push'


class Type(models.TextChoices):
    SIGN_UP = 'email', 'Email'
    REVIEW_LIKE = 'sms', 'SMS'
    NEW_FILM = 'new_film', 'Mew film'
    BOOKMARKS = 'bookmarks', 'Bookmarks'
    INFO = 'info', 'Info'


class Notification(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=Type.choices)
    channel = models.CharField(max_length=255, choices=Chanel.choices)
    user = models.CharField(max_length=255, null=True, blank=True)
    user_group = models.CharField(max_length=255, null=True, blank=True)
    template = models.TextField(help_text="Шаблон сообщения для email или текста")
    # cron_schedule = models.CharField(max_length=100, blank=True, null=True, help_text="Crontab выражение для периодической задачи")
    # api_url = models.URLField(help_text="URL внешнего API для отправки данных")
    created_at = models.DateTimeField(auto_now_add=True)
    # last_run_at = models.DateTimeField(null=True, blank=True)
    context = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.task_name}"
