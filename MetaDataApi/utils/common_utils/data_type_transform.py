import logging
from datetime import datetime

import dateutil
import dateutil.parser
from dateutil.parser._parser import ParserError

logger = logging.getLogger(__name__)


def try_transform_to_float(elm):
    if "." in elm:
        return float(elm)
    else:
        raise ValueError("does not contain decimal separator")


def try_transform_to_bool(elm):
    trues = ("true", "True")
    falses = ("false", "False")
    if elm in trues:
        return True
    elif elm in falses:
        return False
    else:
        raise ValueError("is not either true or false")


def try_transform_to_datetime(text):
    try:
        return dateutil.parser.parse(text)
    except ParserError:
        datetime_formats = (
            '%Y-%m-%dT%H: %M: %SZ',  # strava
        )
        for fmt in datetime_formats:
            try:
                return datetime.strptime(text, fmt)
            except ValueError as e:
                pass
        raise ValueError('no valid date format found')


transform_methods = {
    float: try_transform_to_float,
    int: lambda elm: int(elm),
    datetime: try_transform_to_datetime,
    str: lambda elm: str(elm),
    bool: try_transform_to_bool
}


def transform_data_type(element):
    if element is None:
        return None
    # even though it is a string,
    # it might really be a int or float
    # so if string verify!!
    if isinstance(element, str):
        order = [float, int, datetime, bool, str]
        for typ in order:
            try:
                # try the converting function of that type
                # if it doesnt fail, thats our type
                return transform_methods[typ](element)
            except ValueError as e:
                logger.debug(f"failed with error msg: {e}")
        # if nothing else works, return as string
        return str(element)

    elif isinstance(element, (float, int, bool)):
        # otherwise just return the type of
        return element
