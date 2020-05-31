from MetaDataApi.utils import DjangoModelEnum
from dataproviders.services.url_args_formatter.args_rule_formatters.time_utc_sec import TimeUtcSec
from dataproviders.services.url_args_formatter.args_rule_formatters.time_y_d_m import TimeYMD


class UrlArgFormatter(DjangoModelEnum):
    NONE = None
    TIME_UTC_SEC = TimeUtcSec
    TIME_Y_M_D = TimeYMD
