from MetaDataApi.utils import DjangoModelEnum
from dataproviders.services.url_args_formatter.args_rule_types import *


class UrlArgType(DjangoModelEnum):
    AUTH_TOKEN = AuthToken
    START_DATE_TIME = StartDateTime
    END_DATE_TIME = EndDateTime
    PAGE_CURRENT = PageCurrent
    PAGE_SIZE = PageSize
