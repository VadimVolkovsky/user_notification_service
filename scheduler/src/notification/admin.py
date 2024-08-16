from django.contrib import admin
from .models import Notification

from tasks import task_send_admin_notification


@admin.register(Notification)
class NotificationTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'created_at')
    search_fields = ('title', 'recipients')
    actions = ['send_notifications']

    def send_notifications(self, request, queryset):
        for notification in queryset:
            task_send_admin_notification.delay(notification.id)
            notification.status = 'Sent'
            notification.save()
