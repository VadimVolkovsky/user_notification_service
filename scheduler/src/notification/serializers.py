import json

from django.core.serializers import serialize


def notification_serializer(notification):
    notification_json = serialize('json', [notification])
    notification_json = json.loads(notification_json)[0]['fields']
    return notification_json
