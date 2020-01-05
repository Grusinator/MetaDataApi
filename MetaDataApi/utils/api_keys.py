import json
import logging
import os

logger = logging.getLogger(__name__)

api_keys_filename = 'api_keys.json'


def read_api_keys():
    try:
        with open(api_keys_filename) as f:
            return json.load(f)
    except FileNotFoundError as e:
        logger.warning("api_keys.json was not found")
    except Exception as e:
        logger.warning("could not read api_keys.json")
    return {}


api_keys = read_api_keys()


def get_setting_from_env_var_or_json_file(var_name):
    return os.environ.get(var_name) or api_keys.get(var_name)
