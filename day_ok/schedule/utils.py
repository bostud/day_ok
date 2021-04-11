import pytz
import re
from typing import Union, Optional, List, Tuple
from datetime import datetime, date, timedelta, time


WEEK_DAYS_NAMES_UA = {
    1: 'Понеділок',
    2: 'Вівторок',
    3: 'Середа',
    4: 'Четвер',
    5: 'Пʼятниця',
    6: 'Субота',
    7: 'Неділя',
}

DAY_TIME_START = time(hour=8)
DAY_TIME_END = time(hour=21)

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


def datetime_localize(dt: datetime) -> datetime:
    return pytz.timezone('Europe/Kiev').localize(dt)


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


def get_period_months_start_end(
    dt_from: datetime,
    dt_until: Optional[datetime] = None,
) -> List[Optional[Tuple[datetime, datetime]]]:
    if not dt_until:
        dt_until = datetime_now_tz()
    else:
        dt_until = datetime_localize(dt_until)
    dt_from = datetime_localize(dt_from)
    months = get_month_from_date(dt_from, dt_until)
    res = []
    month_counter = 0
    for y in range(dt_from.year, dt_until.year + 1):
        for m in range(1, 13):
            dt_start = datetime(year=y, month=m, day=1)
            res.append((
                dt_start,
                create_datetime_end_period(dt_start) - timedelta(days=1),
            ))
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


def create_datetime_start_period(dt: datetime):
    return datetime(
        year=dt.year,
        month=dt.month,
        day=1
    )


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


def get_day_time_periods() -> List[time]:
    res = []
    for hour in range(DAY_TIME_START.hour, DAY_TIME_END.hour):
        for minutes in [0, 30]:
            res.append(time(hour, minutes))
    return res


def get_live_time_period() -> time:
    time_ = datetime_now_tz().time()
    return (
        time(
            time_.hour,
            0 if time_.minute < 30 else 30,
            0,
        )
    )


def get_first_date_of_month(dt: datetime = None, return_str: bool = True) -> str:
    dt = datetime_now_tz() if not dt else dt
    dt = date(dt.year, dt.month, 1)
    if return_str:
        return dt.strftime('%d.%m.%Y')
    else:
        return dt


def get_last_date_of_month(dt: datetime = None, return_str: bool = True) -> str:
    dt = datetime_now_tz() if not dt else dt
    next_month = get_next_month_from_date(dt)
    dt = (next_month - timedelta(days=1)).date()
    if return_str:
        return dt.strftime('%d.%m.%Y')
    else:
        return dt


def get_week_date_start(dt: date) -> date:
    return dt - timedelta(days=get_weekday_number(dt)-1)
