import random

import os
import json
from django.conf import settings
from datetime import datetime, timedelta


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
    def loadStravaActivities(cls):
        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())
        return data
