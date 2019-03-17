import random
from datetime import datetime, timedelta

from metadata.models import BaseInstance


class UtilsForTesting:

    @staticmethod
    def mutate(input_list):
        filtered_list = list(filter(
            lambda x: isinstance(x, (str, float, int, bool, datetime)),
            input_list))

        if len(filtered_list) == 0:
            raise ValueError("there is no values to mutate")

        # get indexes
        indexes = [input_list.index(x) for x in filtered_list]

        output_list = input_list.copy()

        # select a mutation value
        idx = random.choice(indexes)

        mutating_obj = input_list[idx]

        if isinstance(mutating_obj, str):
            output_list[idx] = input_list[idx] + "_mutated"
        elif isinstance(mutating_obj, bool):
            output_list[idx] = not input_list[idx]
        elif isinstance(mutating_obj, (int, float)):
            output_list[idx] = input_list[idx] + 3
        elif isinstance(mutating_obj, datetime):
            output_list[idx] = input_list[idx] + timedelta(0, 3)

        return output_list

    @classmethod
    def build_meta_instance_strings_for_comparison(cls, instances):
        labels = list(map(cls.build_meta_instance_string_signature, instances))
        return cls.sort_and_remove_duplicates(labels)

    @staticmethod
    def build_meta_instance_string_signature(obj):
        from metadata.models import BaseAttributeInstance

        label = obj.base.label if isinstance(obj, BaseInstance) else obj.label

        signature = "%s - %s" % (label, str(type(obj).__name__))
        if isinstance(obj, BaseAttributeInstance):
            signature += " : %s" % obj.value
        return signature

    @staticmethod
    def sort_and_remove_duplicates(labels):
        labels = list(set(labels))
        labels.sort()
        return labels
