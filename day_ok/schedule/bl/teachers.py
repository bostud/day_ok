from typing import Optional, List, Tuple, Generator
from ..models import Teacher, Subject, Lessons
from datetime import datetime, timedelta
from ..utils import datetime_now_tz, get_last_date_of_month, get_weekday_number
from dataclasses import dataclass
from ..data_classes.teachers import DailyLessonsReport, WeeklyLessonsReport


@dataclass
class SubjectReport:
    subject: Subject
    count: int
    lessons: List[Lessons]


@dataclass
class LessonsReport:
    lessons_type_name: str
    lessons_type_id: int
    count: int
    subjects_reports: List[SubjectReport]

    @property
    def is_individual(self):
        return int(self.lessons_type_id) == Lessons.Type.INDIVIDUAL


def teachers_objects() -> List[Optional[Teacher]]:
    return Teacher.objects.filter(
        record_status=Teacher.RecordStatus.ACTIVE,
    ).order_by(
        'first_name'
    ).order_by(
        'last_name'
    ).all()


def get_teacher(teacher_id: int) -> Optional[Teacher]:
    return Teacher.objects.filter(
        id=teacher_id,
        record_status=Teacher.RecordStatus.ACTIVE,
    ).first()


def get_teacher_lessons_info(
    teacher_id: int,
    date_start: datetime,
    date_end: datetime,
) -> List[Optional[LessonsReport]]:
    t = Teacher.objects.filter(id=teacher_id).first()
    res = []
    if t:
        for type_id, type_name in Lessons.Type.choices:
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


def set_teacher_lessons_color(
    teacher_id: int,
    color: str,
    font_color: int,
) -> Optional[Teacher]:
    teacher = Teacher.objects.filter(id=teacher_id).first()

    if teacher:
        teacher.lessons_color = color
        teacher.lessons_font_color = font_color
        teacher.save()

    return teacher


def add_teacher(
    first_name: str,
    last_name: str,
    phone_number: str,
    email: str,
    date_of_birth: datetime.date,
    date_start: datetime.date,
    subjects: List[int],
    status: Optional[int],
) -> Teacher:
    t: Optional[Teacher] = Teacher.objects.create(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        email=email,
        date_start=date_start,
        date_of_birth=date_of_birth,
    )
    if subjects:
        t.subjects.add(
            *list(Subject.objects.filter(id__in=[int(v) for v in subjects]).all())  # noqa: E501
        )
    if status:
        t.status = status
    t.save()
    return t


def edit_teacher(
    teacher_id: int,
    first_name: str,
    last_name: str,
    phone_number: str,
    email: str,
    date_of_birth: datetime.date,
    date_start: datetime.date,
    subjects: List[int],
    status: Optional[int],
) -> Optional[Teacher]:
    if t := Teacher.objects.filter(id=teacher_id).first():
        t.first_name = first_name
        t.last_name = last_name
        t.phone_number = phone_number
        t.email = email
        t.date_start = date_start
        t.date_of_birth = date_of_birth
        if subjects:
            t.subjects.add(
                *list(Subject.objects.filter(id__in=[int(v) for v in subjects]).all())  # noqa
            )
        if status:
            if int(status) == Teacher.Status.RELEASE.value:
                t.date_release = datetime_now_tz()
            else:
                t.date_release = None
            t.status = status
        t.date_update = datetime_now_tz()
        t.save()
    return t


def prepare_date_fields(data: dict) -> dict:
    fields = ['date_of_birth', 'date_start', 'date_release']
    for f in fields:
        if v := data.get(f):
            data[f] = v.strftime('%d.%m.%Y')
    return data


def delete_teacher(
    teacher_id: int,
) -> int:
    t: Optional[Teacher] = Teacher.objects.filter(id=teacher_id).first()
    dt_now = datetime_now_tz()
    if t:
        if lessons := Lessons.objects.filter(teacher=t, date__gt=dt_now.date()).all():
            lessons.delete()
        if not Lessons.objects.filter(teacher=t).all():
            t.delete()
        else:
            t.status = Teacher.Status.INACTIVE
            t.record_status = Teacher.RecordStatus.DELETED
            t.save()
        return 1
    return 0


def unpin_teacher_subject(
    teacher_id: int,
    subject_id: int,
) -> Optional[Teacher]:
    t: Optional[Teacher] = Teacher.objects.filter(id=teacher_id).first()
    if t and t.subjects:
        s: Optional[Subject] = Subject.objects.filter(id=int(subject_id)).first()  # noqa
        if s:
            dt_now = datetime_now_tz()
            Lessons.objects.filter(
                teacher=t,
                subject=s,
                date__gt=dt_now.date(),
            ).delete()
            if not (
                Lessons.objects.filter(
                    teacher=t,
                    subject=s,
                    date__lte=dt_now.date(),
                ).all()
            ):
                t.subjects.remove(s)
        t.save()
    return t


def get_lessons_by_date(
    dt: datetime.date,
    teacher: Teacher,
) -> List[Optional[Lessons]]:
    return Lessons.objects.filter(
        date=dt,
        teacher=teacher,
    ).order_by('time_start').all()


def get_lessons_by_year_and_month(
    teacher: Teacher,
    year: int,
    month: int,
) -> Tuple[datetime.date, List[Optional[Lessons]]]:
    _date = datetime(year=year, month=month, day=1)
    _last_date = get_last_date_of_month(_date, return_str=False).date()
    _date = _date.date()
    while _date <= _last_date:
        yield _date, get_lessons_by_date(_date, teacher)
        _date = _date + timedelta(days=1)


def get_weekly_lessons_by_year_and_month(
    teacher: Teacher,
    year: int,
    month: int,
) -> Generator:
    _date = datetime(year=year, month=month, day=1)
    _last_date = get_last_date_of_month(_date, return_str=False)
    _date = _date.date() - timedelta(days=get_weekday_number(_date) - 1)
    week_day = 0
    result = []
    while _date <= _last_date:
        daily_r = DailyLessonsReport(
            get_lessons_by_date(_date, teacher),
            _date,
            _date.month == month,
        )
        result.append(daily_r)
        week_day += 1
        _date = _date + timedelta(days=1)

        if week_day == 7:
            yield WeeklyLessonsReport(
                1,
                _date - timedelta(days=week_day),
                _date,
                result
            )
            week_day = 0
            result = []

    yield WeeklyLessonsReport(
        1,
        _date - timedelta(days=week_day),
        _date,
        result
    )


