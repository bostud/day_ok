from datetime import date
from ..utils import get_days_from_date
from ..models import Event


def get_weekly_class_room_events_by_day(
    class_room_id: int,
    date_from: date,
) -> dict:
    result = {}
    days = get_days_from_date(date_from)
    for d in days:
        lessons = Event.objects.filter(
            date_of_event=d,
            class_room__id=class_room_id,
        ).order_by('time_start').all()

        result[d.strftime('%d.%m.%Y')] = list(lessons)

    return result
