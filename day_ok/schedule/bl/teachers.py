from typing import Optional, List
from ..models import Teacher, Subject, Lessons, LESSONS_TYPES, INDIVIDUAL
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class SubjectReport:
    subject: Subject
    count: int
    lessons: List[Lessons]


@dataclass
class LessonsReport:
    lessons_type_name: str
    lessons_type_id: str
    count: int
    subjects_reports: List[SubjectReport]

    @property
    def is_individual(self):
        return self.lessons_type_id == INDIVIDUAL


def teachers_objects() -> List[Optional[Teacher]]:
    return Teacher.objects.order_by('first_name').order_by('last_name').all()


def get_teacher(teacher_id: int) -> Optional[Teacher]:
    return Teacher.objects.filter(
        id=teacher_id
    ).first()


def get_teacher_lessons_info(
    teacher_id: int,
    date_start: datetime,
    date_end: datetime,
) -> List[Optional[LessonsReport]]:
    t = Teacher.objects.filter(id=teacher_id).first()
    res = []
    if t:
        for type_id, type_name in LESSONS_TYPES:
            subject_res = []
            count = 0
            for subject in t.subjects.all():
                lessons = Lessons.objects.filter(
                    teacher=t,
                    lessons_type=type_id,
                    date__gte=date_start.date(),
                    date__lt=date_end,
                    subject=subject,
                ).order_by('time_start').order_by('date')
                c = lessons.count()
                count += c
                subject_res.append(
                    SubjectReport(
                        lessons=lessons.all(),
                        count=c,
                        subject=subject,
                    )
                )
            res.append(
                LessonsReport(
                    lessons_type_name=type_name,
                    lessons_type_id=type_id,
                    subjects_reports=subject_res,
                    count=count
                )
            )

    return res

