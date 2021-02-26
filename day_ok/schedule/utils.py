import pytz
import re
from typing import Union, Optional, List, Tuple
from datetime import datetime, date, timedelta


WEEK_DAYS_NAMES_UA = {
    1: 'Понеділок',
    2: 'Вівторок',
    3: 'Середа',
    4: 'Четвер',
    5: 'Пʼятниця',
    6: 'Субота',
    7: 'Неділя',
}

DATE_START_PERIODS = datetime(year=2021, month=1, day=1)
PERIOD_REGEXP = re.compile(r'^(\d{4})\.(1|2|3|4|5|6|7|8|9|10|11|12)$')


def get_weekday_number(dt: Union[datetime, date]) -> Optional[int]:
    try:
        return dt.weekday() + 1
    except (ValueError, TypeError):
        return None


def get_weekday_name(day_number: int) -> Optional[str]:
    return WEEK_DAYS_NAMES_UA.get(day_number)


def get_weekday_name_by_date(dt: Union[datetime, date]) -> Optional[str]:
    return get_weekday_name(
        get_weekday_number(dt)
    )


def get_days_from_date(
    date_start: date,
    days_forward: int = 7,
) -> List[date]:
    if days_forward == 0:
        days_forward += 1
    return [
        date_start + timedelta(days=i)
        for i in range(days_forward)
    ]


def get_month_from_date(
    date_start: datetime,
    date_end: datetime,
) -> int:
    return (
        date_end.year - date_start.year
    ) * 12 + (
        date_end.month - date_start.month
    ) + 1


def get_weekdays_tuple() -> Tuple[Tuple[int, str]]:
    return tuple((id_, name) for id_, name in WEEK_DAYS_NAMES_UA.items())


def datetime_now_tz() -> datetime:
    return datetime.now(tz=pytz.timezone('Europe/Kiev'))


def get_year_month_periods() -> List[str]:
    dt_now = datetime_now_tz()
    dt_start = DATE_START_PERIODS
    months = get_month_from_date(dt_start, dt_now)
    res = []
    month_counter = 0
    for y in range(dt_start.year, dt_now.year + 1):
        for m in range(1, 13):
            res.append(f"{y}.{m}")
            month_counter += 1
            if month_counter == months:
                return res

    return res


def get_period(year: int, month: int) -> str:
    assert 1 <= month <= 12
    return f"{year}.{month}"


def is_valid_period_format(period: str) -> bool:
    match = PERIOD_REGEXP.search(period)
    if match:
        return True
    return False


def create_datetime_start_from_period(period: str):
    if is_valid_period_format(period):
        match = PERIOD_REGEXP.search(period)
        return datetime(
            year=int(match.group(1)),
            month=int(match.group(2)),
            day=1
        )
    return DATE_START_PERIODS


def create_datetime_end_period(dt_start: datetime):
    return get_next_month_from_date(dt_start)


def get_next_month_from_date(dt_from: datetime) -> datetime:
    if dt_from.month == 12:
        return datetime(
            year=dt_from.year + 1,
            month=1,
            day=1
        )
    else:
        return datetime(
            year=dt_from.year,
            month=dt_from.month + 1,
            day=1,
        )
