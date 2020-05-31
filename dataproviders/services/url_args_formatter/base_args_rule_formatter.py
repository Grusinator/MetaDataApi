from abc import ABC, abstractmethod

from dataproviders.services.url_args_formatter.base_url_arg_formatting_rule import BaseUrlArgValue


class BaseArgsRuleFormatter(ABC):

    @staticmethod
    @abstractmethod
    def convert(base_url_arg_value: BaseUrlArgValue):
        raise NotImplementedError
