import logging
from typing import List
from datetime import date, timedelta
from ..models import Lessons, StudentPresence, INDIVIDUAL

log = logging.getLogger(__name__)


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
        for les in lessons:
            les.presence_count = (
                StudentPresence.objects.filter(lessons=les).count())
            if les.lessons_type == INDIVIDUAL:
                les.students_count = 1
            else:
                les.students_count = les.group.students.count()
        result[d.strftime('%d.%m.%Y')] = list(lessons)

    return result


def get_seven_days_from_date(
    date_start: date,
) -> List[date]:
    return [
        date_start + timedelta(days=i)
        for i in range(7)
    ]


def all_presence(lessons_id: int):
    lessons = Lessons.objects.get(id=lessons_id)
    if lessons.lessons_type == INDIVIDUAL:
        students = [lessons.student] if lessons.student else []
    else:
        students = [st for st in lessons.group.students.all()]

    for student in students:
        _, created = StudentPresence.objects.get_or_create(
            student=student,
            lessons=lessons
        )
        if created:
            log.info(
                f'Create presence for student: {str(student)}/{student.id}. '
                f'Lessons {str(lessons)}/{lessons_id}'
            )
