import random

import os
import json
from django.conf import settings
from datetime import datetime, timedelta


class UtilsForTesting:

    @staticmethod
    def mutate(input_list):
        if not any([isinstance(elm, (str, float, int, bool))for elm in input_list]):
            raise ValueError("there is no values to mutate")

        filtered_list = list(filter(
            lambda x: isinstance(x, (str, float, int, bool), input_list)))

        # get indexes
        indexes = [input_list.index(x) for x in filtered_list]

        # select a mutation value
        idx = random.choice(indexes)

        mutating_obj = input_list[idx]

        if isinstance(mutating_obj, str):
            input_list[idx] += "_mutated"
        elif isinstance(mutating_obj, bool):
            input_list[idx] = not input_list[idx]
        elif isinstance(mutating_obj, (int, float)):
            input_list[idx] += 3
        elif isinstance(mutating_obj, datetime):
            input_list[idx] += timedelta(0, 3)

        return input_list

    @classmethod
    def loadStravaActivities(cls):
        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())
        return data
