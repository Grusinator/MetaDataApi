from dataproviders.models import DataProvider


# from metadata.rdfs_models.rdfs_data_provider import RdfsDataProvider


def CreateRdfsDataProviderEndpointService(provider_name, url, endpoint_name):
    provider = DataProvider.exists(provider_name)
    raise NotImplementedError
    # RdfsDataProvider.create_endpoint_to_data_provider(
    #     provider.data_provider_instance,
    #     endpoint_url=url,
    #     endpoint_name=endpoint_name
    # )


def CreateRdfsDataProviderService(provider_name, endpoint_name, file):
    provider = DataProvider.exists(provider_name)
    raise NotImplementedError
    # rest_endpoint = RdfsDataProvider._get_endpoint(provider.data_provider_instance, rest_endpoint_name)
    # RdfsDataProvider.create_data_dump(rest_endpoint, file)
