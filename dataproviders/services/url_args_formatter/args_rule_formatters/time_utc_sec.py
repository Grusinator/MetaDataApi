from dataproviders.services.url_args_formatter.base_args_rule_formatter import BaseArgsRuleFormatter
from dataproviders.services.url_args_formatter.base_url_arg_formatting_rule import BaseUrlArgValue


class TimeUtcSec(BaseArgsRuleFormatter):

    @staticmethod
    def convert(base_url_arg_value: BaseUrlArgValue):
        return str(int(base_url_arg_value.value.timestamp()))
