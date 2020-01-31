from django.apps import AppConfig


class DynamicModelsConfig(AppConfig):
    name = 'dynamic_models'

    def ready(self):
        from dynamic_models.tasks import connect_tasks
        connect_tasks()
        from dynamic_models.tests.test_graphene_schema import create_dummy_model_def
        create_dummy_model_def()
