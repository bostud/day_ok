from typing import Union, Optional
from datetime import datetime, date

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
