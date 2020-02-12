from django.apps import AppConfig


class DynamicModelsConfig(AppConfig):
    name = 'dynamic_models'

    def ready(self):
        from dynamic_models.attach_tasks import attach_tasks
        attach_tasks()
