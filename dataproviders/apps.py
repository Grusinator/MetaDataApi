from django.apps import AppConfig


class DataprovidersConfig(AppConfig):
    name = 'dataproviders'

    def ready(self):
        from dataproviders.tasks import connect_tasks
        connect_tasks()
