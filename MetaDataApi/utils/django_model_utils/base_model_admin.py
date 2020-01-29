from importlib import import_module, reload

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.urls import clear_url_caches


class BaseModelAdmin(admin.ModelAdmin):
    actions = []
    model = None

    @classmethod
    def add_action_from_single_arg_method(cls, method, method_name=None):
        action_method = cls.turn_method_into_action_method(method)
        cls.add_action(action_method, method_name)

    @classmethod
    def add_action(cls, method, method_name=None):
        method_name = method_name or method.__name__
        cls.actions.append(method_name)
        setattr(cls, method_name, method)
        cls.reload_admin_model()

    @classmethod
    def reload_admin_model(cls):
        try:
            admin.site.unregister(cls.model)
        except NotRegistered:
            pass

        admin.site.register(cls.model, cls)
        cls.reload_and_clear_cache_admin()

    @classmethod
    def reload_and_clear_cache_admin(cls):
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()

    @classmethod
    def turn_method_into_action_method(cls, method):
        """
        :param method: must be a method that only takes one model object
        :return: a method that can be inserted as action into BaseModelAdmin.add_action( )
        """

        def action(self, request, queryset):
            for elm in queryset:
                method(elm)

        action.__name__ = method.__name__
        return action
