import json
import logging

logger = logging.getLogger(__name__)

api_keys = {}
try:
    with open('api_keys.json') as f:
        api_keys = json.load(f)
except FileNotFoundError as e:
    logger.warning("api_keys.json was not found")
except Exception as e:
    logger.warning("could not read api_keys.json")
