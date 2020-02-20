from dataproviders.models.DataFileSourceBase import DataFileSourceBase

data_file_upload_on_save_methods = []


class DataFileUpload(DataFileSourceBase):

    class Meta(DataFileSourceBase.Meta):
        default_related_name = '%(model_name)s'

    def execute_on_save_methods(self):
        for method in data_file_upload_on_save_methods:
            method(self)
