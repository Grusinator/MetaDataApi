# import unittest
# from functools import wraps
#
# from django.conf import settings
#

# def add_test_tag(tags):
#     func = lambda x: unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & tags, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
#     return func
#     def real_decorator(function):
#         @wraps(function)
#         def wrapper(*args, **kwargs):
#             funny_stuff()
#             something_with_argument(argument)
#             retval = function(*args, **kwargs)
#             more_funny_stuff()
#             return retval
#
#         return wrapper
#
#     return real_decorator
