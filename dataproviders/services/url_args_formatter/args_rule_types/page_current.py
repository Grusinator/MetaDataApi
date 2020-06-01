from dataproviders.services.url_args_formatter.base_url_arg_formatting_rule import BaseUrlArgValue


class PageCurrent(BaseUrlArgValue):
    def __init__(self, value, elements_pr_page=1):
        # TODO this should be a formatter instead
        value = value * elements_pr_page
        super().__init__(value)

    pass
