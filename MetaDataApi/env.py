from enum import Enum


class Env(Enum):
    PROD = "PROD"
    DEV = "DEV"
    LOCAL = "LOCAL"
    TEST = "TEST"

    def get_url(self):
        return url_mapper[self]


url_mapper = {
    # "PROD": "https://meta-data-api.herokuapp.com/",
    # "DEV": "https://meta-data-api-dev.herokuapp.com/",
    Env.PROD: "http://metadataapi.grusinator.com/",
    Env.DEV: "http://metadataapi.wsh-home.dk:8000/",
    Env.LOCAL: "http://localhost:8000/",
    Env.TEST: "http://localhost:8000/"
}
