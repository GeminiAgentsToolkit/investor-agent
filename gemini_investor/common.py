from zoneinfo import ZoneInfo
from datetime import datetime
from dateutil import parser


NASDAQ_TZ=ZoneInfo("America/New_York")


def now():
    return datetime.now(tz=NASDAQ_TZ)


def parse_date(date_str):
    return parser.parse(date_str, tzinfos={'': NASDAQ_TZ})