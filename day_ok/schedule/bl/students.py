from typing import List, Optional
from ..models import Student, Lessons, Group, Invoice
from ..utils import datetime_now_tz as now

from django.db.models import Q


def get_students() -> List[Student]:
    return Student.objects.order_by('first_name').order_by('last_name').all()


def get_student(id_: int) -> Optional[Student]:
    return Student.objects.filter(id=id_).first()


def get_student_future_lessons(
    student_id: int,
    count: int = 5,
) -> List[Optional[Lessons]]:
    dt_now = now()
    lessons = Lessons.objects.filter(
        Q(student_id=student_id) | Q(group__students__in=[student_id]),
        date__gte=dt_now.date(),
    ).order_by('time_end').order_by('date')[:count]
    return list(filter(lambda l: not l.is_finished, lessons))


def get_student_all_lessons(
    student_id: int,
) -> List[Optional[Lessons]]:
    return Lessons.objects.filter(
        Q(student_id=student_id) | Q(group__students__in=[student_id]),
    ).order_by('time_start').order_by('-date')


def get_student_groups(
    student_id: int,
) -> List[Optional[Group]]:
    return Group.objects.filter(
        students__in=[Student.objects.filter(id=student_id).first()]
    )


def get_student_invoices(
    student_id: int,
) -> List[Optional[Invoice]]:
    return Invoice.objects.filter(
        student_id=student_id
    ).order_by(
        '-date_created'
    )
