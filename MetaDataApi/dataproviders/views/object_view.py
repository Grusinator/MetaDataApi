import logging

from django.shortcuts import render

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.models import SchemaNode
from MetaDataApi.metadata.models.meta.object_table_view import ObjectTableView

logger = logging.getLogger(__name__)


def object_view(request, provider_name, object_label):
    dataprovider = DataProvider.objects.get(provider_name=provider_name)
    selected_schema = dataprovider.get_schema_for_provider()
    selected_object = SchemaNode.exists_by_label(object_label, selected_schema.label)
    object_view = ObjectTableView(selected_object)

    return render(
        request,
        'object.html',
        {
            "object_view": object_view
        }
    )
