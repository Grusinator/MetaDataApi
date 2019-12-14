# class StoreDataFromProviderService(Service):
#     """Read the raw data from endpoint"""
#
#     provider_name = forms.CharField()
#     endpoint_name = forms.CharField(required=False)
#     user_pk = forms.IntegerField()
#
#     def process(self):
#         provider_name = self.cleaned_data['provider_name']
#         endpoint_name = self.cleaned_data['endpoint_name']
#         user_pk = self.cleaned_data['user_pk']
#         user = User.objects.get(pk=user_pk)
#
#         data_provider = DataProvider.objects.get(
#             provider_name=provider_name)
#
#         service = FetchDataFromProvider(data_provider)
#         # get the profile, with the access token matching the provider_name
#         thirdpartyprofiles = user.data_provider_users
#         thirdpartyprofile = thirdpartyprofiles.get(
#             data_provider__provider_name=provider_name)
#
#         data = service._fetch_data_from_endpoint(
#             endpoint_name, thirdpartyprofile.access_token)
#
#         data = JsonUtils.clean(data)
#
#         service._save_data_to_file(endpoint_name, data)
#
#         return data
