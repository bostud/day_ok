from typing import List, Optional
from datetime import date
from ..models import Teacher, Lessons
from ..data_classes.finance import TeacherMonthStat, TeacherSubjectStat
from ..utils import get_first_date_of_month, get_last_date_of_month
from .teachers import teachers_objects

GROUP_LESSONS_PRICE_UAH = 250


def get_teachers_month_statistics(
    date_start: date = None,
    date_end: date = None,
) -> List[Optional[TeacherMonthStat]]:
    date_start = date_start or get_first_date_of_month(return_str=False)
    date_end = date_end or get_last_date_of_month(return_str=False)
    if date_end < date_start:
        date_end = get_last_date_of_month(date_start)

    for teacher in teachers_objects():
        if teacher.date_release and teacher.date_release.date() < date_start:
            continue

        subjects_stat = []
        for subject in teacher.subjects.all():
            group_lessons = [ls for ls in Lessons.objects.filter(
                lessons_type=Lessons.Type.GROUP,
                date__gte=date_start,
                date__lte=date_end,
                teacher=teacher,
                subject=subject,
            )]

            individual_lessons = [ls for ls in Lessons.objects.filter(
                lessons_type=Lessons.Type.INDIVIDUAL,
                date__gte=date_start,
                date__lte=date_end,
                teacher=teacher,
                subject=subject,
            )]

            subjects_stat.append(
                TeacherSubjectStat(
                    subject=subject,
                    individual_lessons=individual_lessons,
                    group_lessons=group_lessons,
                )
            )

        yield TeacherMonthStat(
            teacher=teacher,
            subjects_stat=subjects_stat,
        )
