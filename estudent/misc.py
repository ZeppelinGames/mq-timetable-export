
from enum import IntEnum, IntFlag
from bs4 import BeautifulSoup, SoupStrainer

HTML_PARSER = 'html.parser'
TZ = 'Australia/Sydney'
LOGIN_URL = 'https://student1.mq.edu.au/T1SMPROD/WebApps/eStudent'
TIMETABLE_URL = 'https://mq-edu-web.t1cloud.com/T1SMDefault/WebApps/eStudent/SM/StudentTtable10.aspx?r=MQ.ESTU.UGSTUDNTB&f=MQ.EST.TIMETBL.WEB'

ClassFlags = IntFlag('ClassFlags', 'registered swappable stream')
Day = IntEnum('DayOfWeek', 'sun mon tue wed thu fri sat', start=0)
DAY_NAMES = tuple('Sunday Monday Tuesday Wednesday Thursday Friday Saturday'.split())
DAY_NAME_LOOKUP = dict(zip(Day, DAY_NAMES))
DAY_ENUM_LOOKUP = dict(zip(DAY_NAMES, Day))


def make_soup(markup, strain=None):
    if strain is None:
        strain = {}
    return BeautifulSoup(markup, HTML_PARSER, parse_only=SoupStrainer(**strain))
