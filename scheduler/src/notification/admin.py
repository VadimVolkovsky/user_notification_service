from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'user', 'created_at')
    search_fields = ('title', 'user', 'user_group')
