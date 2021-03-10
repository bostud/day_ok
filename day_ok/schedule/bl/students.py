from typing import List, Optional
from ..models import Student, Lessons
from ..utils import datetime_now_tz as now

from django.db.models import Q


def get_students() -> List[Student]:
    return Student.objects.order_by('first_name').order_by('last_name').all()


def get_student(id_: int) -> Optional[Student]:
    return Student.objects.filter(id=id_).first()


def get_student_lessons(
    student_id: int,
    count: int = 5,
) -> List[Optional[Lessons]]:
    dt_now = now()
    return Lessons.objects.filter(
        Q(student_id=student_id) | Q(group__students__in=[student_id]),
        date__gte=dt_now.date(),
        time_end__gte=dt_now.time(),
    ).order_by('time_end').order_by('date')[:count]
