from django.db import models


# from json2model.services.dynamic_model import create_objects_from_json, create_instances_from_json
# from jsonfield import JSONField
#
#
# class CreateRequest(models.Model):
#     root_name = models.TextField()
#     json_data = JSONField()
#     status = models.IntegerField(default=0)
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         create_objects_from_json(self.root_name, self.json_data)
#         create_instances_from_json(self.root_name, self.json_data)

class Dummy(models.Model):
    name = models.TextField()
