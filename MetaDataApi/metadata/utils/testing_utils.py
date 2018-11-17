import os
import json
from django.conf import settings


class TestingUtils:

    @classmethod
    def loadStravaActivities():
        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())
        return data
