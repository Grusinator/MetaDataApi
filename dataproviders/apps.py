from django.apps import AppConfig


class DataprovidersConfig(AppConfig):
    name = 'dataproviders'

    def ready(self):
        from dataproviders.attach_tasks import attach_tasks
        attach_tasks()
