import pytz
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


def get_weekdays_tuple() -> Tuple[Tuple[int, str]]:
    return tuple((id_, name) for id_, name in WEEK_DAYS_NAMES_UA.items())


def datetime_now_tz() -> datetime:
    return datetime.now(tz=pytz.timezone('Europe/Kiev'))
