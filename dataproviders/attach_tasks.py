from dataproviders import tasks
from dataproviders.admin import DataFileUploadAdmin, DataFetchAdmin
from dataproviders.models.DataFetch import data_fetch_on_save_methods
from dataproviders.models.DataFileUpload import data_file_upload_on_save_methods
from dataproviders.models.DataProviderUser import data_provider_user_save_methods


def attach_tasks():
    data_provider_user_save_methods.append(tasks.schedule_task_refresh_access_token)

    data_file_upload_on_save_methods.append(tasks.schedule_task_clean_data_from_source_file)
    DataFileUploadAdmin.add_action_from_single_arg_method(tasks.schedule_task_clean_data_from_source_file)

    data_fetch_on_save_methods.append(tasks.schedule_task_clean_data_from_source_file)
    # TODO causeing some unique error
    # DataFetchAdmin.add_action_from_single_arg_method(tasks.schedule_task_clean_data_from_source_file)
