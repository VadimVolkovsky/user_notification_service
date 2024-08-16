from .celery_app import app as celery_app

__all__ = ['celery_app']


def ready(self):
    import notification.tasks
