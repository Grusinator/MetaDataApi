# from abc import ABC
#
# from dataproviders.services.transform_methods.i_json_iterator import IJsonIterator
#
#
# class JsonKeyTransformer(IJsonIterator, ABC):
#     def __init__(self, transform_method):
#         self.transform_method = transform_method
#         super().__init__()
#
#     def transform(self, data):
#         return self.start_iterating_data_structure(data, None)
#
#     def handle_attribute(self, object_ref: dict, attribute_label: str, data):
#         new_attribute_label = self.transform_method(attribute_label)
#         if new_attribute_label != attribute_label:
#             object_label = next(iter(object_ref))
#             object_ref[object_label][new_attribute_label] = object_ref[object_label].pop(attribute_label)
#
#     def pre_handle_object(self, parent_ref: dict, object_label: str, data):
#         if object_label:
#             new_object_label = self.transform_method(object_label)
#             return {new_object_label: data}
#         else:  # only first iteration
#             return data
#
#     def post_handle_object(self, parent_ref, object_ref, data):
#         return object_ref
#
#     def handle_related_object(self, parent_ref: str, related_object_ref: str, object_label,
#                               parent_has_many: bool = False):
#         new_object_label = next(iter(related_object_ref))
#         return related_object_ref
