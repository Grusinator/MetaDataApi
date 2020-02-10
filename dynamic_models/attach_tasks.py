from dataproviders.admin import DataFileAdmin
from dataproviders.models.DataFile import data_file_on_save_methods
from dynamic_models import tasks


def attach_tasks():
    data_file_on_save_methods.append(tasks.run_task_build_models_and_load_data_chained)
    DataFileAdmin.add_action_from_single_arg_method(tasks.run_task_build_models_and_load_data_chained)
