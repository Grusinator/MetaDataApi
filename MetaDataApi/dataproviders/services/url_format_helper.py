import re
from urllib import parse


class UrlFormatHelper:
    valid_url_arg_names = [
        "StartDateTime",
        "EndDateTime",
        "AuthToken"
    ]

    arg_data_type_converter = {
        "UTCSEC": lambda x: str(int(x.timestamp())),
        "Y-M-d": lambda x: x.strftime('%Y-%m-%d'),
        "": lambda x: x
    }

    @classmethod
    def build_args_for_url(cls, endpoint_url, **inserted_arguments) -> str:
        for key in inserted_arguments.keys():
            cls.validate(key)

        output_endpoint = endpoint_url

        url_arg_defs = cls.find_all_url_arg_definitions(endpoint_url)
        for url_arg_name, dataformat in url_arg_defs.items():
            cls.validate(url_arg_name)

            value = inserted_arguments[url_arg_name]
            url_arg_value = cls.convert(value, dataformat)
            output_endpoint = output_endpoint.replace(
                cls.build_url_arg_def(dataformat, url_arg_name),
                url_arg_value
            )

        return output_endpoint

    @classmethod
    def standardize_url(cls, url):
        # remove first slash if exists
        return url[1:] if url[0] == "/" else url

    @classmethod
    def join_urls(cls, base: str, endpoint: str):
        return parse.urljoin(
            cls.standardize_url(base),
            cls.standardize_url(endpoint)
        )

    @classmethod
    def build_url_arg_def(cls, data_format: str, url_arg_name: str):
        cls.validate(url_arg_name)
        return ("{%s-%s}" % (url_arg_name, data_format)) \
            .replace("-", ":")

    @classmethod
    def find_all_url_arg_definitions(cls, endpoint_url: str) -> dict:
        url_arg_defs = re.findall("{(.*?)}", endpoint_url)
        return dict(url_arg_def.split(":") for url_arg_def in url_arg_defs)

    @classmethod
    def convert(cls, data, data_format):
        return cls.arg_data_type_converter[data_format](data)

    @classmethod
    def validate(cls, key):
        assert key in cls.valid_url_arg_names, "invalid args"
