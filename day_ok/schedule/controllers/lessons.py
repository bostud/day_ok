from typing import List
from datetime import date, timedelta
from ..models import Lessons


def get_weekly_class_room_lessons_by_day(
    class_room_id: int,
    date_from: date,
) -> dict:
    result = {}
    seven_days = get_seven_days_from_date(date_from)
    for d in seven_days:
        lessons = Lessons.objects.filter(
            date=d,
            class_room__id=class_room_id,
        ).order_by('time_start').all()
        result[d.strftime('%d.%m.%Y')] = list(lessons)

    return result


def get_seven_days_from_date(
    date_start: date,
) -> List[date]:
    return [
        date_start + timedelta(days=i)
        for i in range(7)
    ]
