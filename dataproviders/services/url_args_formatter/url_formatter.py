from typing import List
from urllib import parse

from django.core.exceptions import ObjectDoesNotExist

from dataproviders.models import Endpoint
from dataproviders.models.UrlArgFormatter import UrlArgFormatter
from dataproviders.models.UrlArgType import UrlArgType
from dataproviders.services.url_args_formatter.base_url_arg_formatting_rule import BaseUrlArgValue


class UrlFormatter:
    arg_data_type_converter = {
        "UTCSEC": lambda x: str(int(x.timestamp())),
        "Y-M-d": lambda x: x.strftime('%Y-%m-%d'),
        "": lambda x: x
    }

    @classmethod
    def new_build_args_for_url(cls, url_arg_formatters: List[BaseUrlArgValue]):
        raise NotImplementedError

    @classmethod
    def build_args_for_url(cls, endpoint: Endpoint, selected_args: List[BaseUrlArgValue]) -> str:
        kwargs = cls.build_kwargs_from_url_arg_values(endpoint, selected_args)
        return cls.build_url_with_args(endpoint.endpoint_url, kwargs)

    @classmethod
    def build_url_with_args(cls, endpoint_url, url_args):
        url_parts = list(parse.urlparse(endpoint_url))
        existing_url_args = dict(parse.parse_qsl(url_parts[4]))
        existing_url_args.update(url_args)
        url_parts[4] = parse.urlencode(existing_url_args)
        return parse.urlunparse(url_parts)

    @classmethod
    def build_kwargs_from_url_arg_values(cls, endpoint, selected_args) -> dict:
        args = {}
        for selected_arg in selected_args:
            try:
                url_arg = endpoint.url_args.get(arg_type=selected_arg.__class__.__name__)
            except ObjectDoesNotExist:
                continue
            if UrlArgType.get_class_from_value(url_arg.arg_type):
                formatter = UrlArgFormatter.get_class_from_value(url_arg.value_formatter)
                if formatter:
                    value = formatter.convert(selected_arg)
                else:
                    value = selected_arg.value
                args[url_arg.key_name] = value
        return args

    @classmethod
    def standardize_url(cls, url: str):
        # remove first slash if exists
        return url[1:] if url[0] == "/" else url

    @classmethod
    def join_urls(cls, base: str, endpoint: str):
        if base == "" or endpoint == "":
            raise Exception("empty string to url join")
        return parse.urljoin(
            cls.standardize_url(base),
            cls.standardize_url(endpoint)
        )