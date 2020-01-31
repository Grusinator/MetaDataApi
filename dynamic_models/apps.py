from django.apps import AppConfig


class DynamicModelsConfig(AppConfig):
    name = 'dynamic_models'

    def ready(self):
        from dynamic_models.tasks import connect_tasks
        connect_tasks()
