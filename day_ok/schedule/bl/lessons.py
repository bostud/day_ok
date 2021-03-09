import logging
import json
from typing import List, Generator
from datetime import date, timedelta, datetime
from ..models import (
    Lessons, StudentPresence,
    ClassRoom, Subject, Teacher, Student, Group, LessonsParent,
    STATUS_TEACHER_ACTIVE,
)
from ..utils import (
    get_days_from_date,
    get_weekday_number,
    get_weekday_name_by_date,
    get_day_time_periods,
)
from ..forms.utils import (
    get_students, get_groups, get_subjects, get_teachers,
    get_classrooms,
)
from ..forms.lessons import (
    AddLessonsForm, EditLessonsForm,
    convert_cleaned_data_to_objects, FilterLessonsForm,
)
from ..data_classes.lessons import AddLessonsDC, EditLessonsDC, EmptyLessons
from ..utils import datetime_now_tz as now, get_weekdays_tuple
from ..data_classes.lessons import LessonsScheduleTeachers

log = logging.getLogger(__name__)


def get_weekly_classroom_lessons_by_classroom(
    classroom_id: int,
    date_from: date,
) -> dict:
    result = {}
    days = get_days_from_date(date_from)
    for d in days:
        lessons = Lessons.objects.filter(
            date=d,
            classroom__id=classroom_id,
        ).order_by('time_start').all()
        result[d.strftime('%d.%m.%Y')] = list(lessons)

    return result


def all_presence(lessons_id: int):
    lessons = Lessons.objects.get(id=lessons_id)
    if lessons.lessons_type == Lessons.Type.INDIVIDUAL:
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


def prepare_add_lessons_form_data() -> dict:
    return AddLessonsDC(
        classrooms=get_classrooms(),
        teachers=get_teachers(),
        students=get_students(),
        groups=get_groups(),
        subjects=get_subjects(),
        weekdays=get_weekdays_tuple(),
        lessons_types=Lessons.Type.choices
    ).to_dict()


def prepare_edit_lessons_form_data(lessons_id: int) -> dict:
    lessons = Lessons.objects.get(id=lessons_id)
    if not lessons:
        return {}
    return EditLessonsDC(
        classroom=lessons.classroom.id,
        teacher=lessons.teacher.id,
        subject=lessons.subject.id,
        student=lessons.student.id if lessons.student else None,
        group=lessons.group.id if lessons.group else None,
        date_from_valid=lessons.date,
        date_until_valid=(
            lessons.parent.date_until_valid
            if lessons.parent else lessons.date
        ),
        time_start=lessons.time_start,
        lessons_type=lessons.lessons_type,
        parent=lessons.parent,
        change_all=True,
        weekdays_for_repeating=(
            lessons.parent.weekdays_list if lessons.parent else [])
    ).to_dict()


def calculate_time_end(
        time_start: datetime.time,
        subject: Subject,
) -> datetime.time:
    date_today = now()
    dt_start = datetime.combine(date_today, time_start)
    datetime_end = dt_start + subject.lessons_duration
    assert date_today.day == datetime_end.day

    return datetime_end.time()


def add_lessons_from_form(form: AddLessonsForm) -> int:
    time_start = form.cleaned_data['time_start']
    subject = Subject.objects.get(id=int(form.cleaned_data['subject']))
    time_end = calculate_time_end(time_start, subject)

    date_until_valid = form.cleaned_data['date_until_valid']
    date_from_valid = form.cleaned_data['date_from_valid']
    weekdays = [int(n) for n in form.cleaned_data['weekdays_for_repeating']]
    classroom = ClassRoom.objects.get(id=int(form.cleaned_data['classroom']))

    teacher = Teacher.objects.get(id=int(form.cleaned_data['teacher']))
    lessons_type = form.cleaned_data['lessons_type']
    if lessons_type == Lessons.Type.INDIVIDUAL:
        student = Student.objects.get(id=int(form.cleaned_data['student']))
        group = None
    else:
        student = None
        group = Group.objects.get(id=int(form.cleaned_data['group']))

    lessons_created = 0
    date_until_valid = date_until_valid or date_from_valid
    assert date_until_valid >= date_from_valid

    parent_lessons = LessonsParent(
        date_from_valid=date_from_valid,
        date_until_valid=date_until_valid,
        weekdays_for_repeating=json.dumps(weekdays),
    )
    for i in range((date_until_valid - date_from_valid).days + 1):
        date_on = date_from_valid + timedelta(days=i)
        day_number = get_weekday_number(date_on)

        # пропуск дня, якщо він не у списку вибраних
        if weekdays and day_number not in weekdays:
            continue

        # add function - check if it free to create lessons
        parent_lessons.save()
        ls = Lessons(
            classroom=classroom,
            date=date_on,
            time_start=time_start,
            time_end=time_end,
            lessons_type=lessons_type,
            subject=subject,
            group=group,
            student=student,
            teacher=teacher,
            parent=parent_lessons,
        )
        ls.save()
        lessons_created += 1

    if lessons_created == 0:
        parent_lessons.delete()

    return lessons_created


def get_weekly_classroom_lessons_by_day(
    date_from: datetime,
) -> dict:
    result = {}
    classrooms = ClassRoom.objects.all()
    for clr in classrooms:
        lessons = Lessons.objects.filter(
            date=date_from,
            classroom__id=clr.id,
        ).order_by('time_start').all()
        result[str(clr.name)] = list(lessons)

    return result


def delete_lessons(lessons_id: int, delete_all: bool):
    lessons = Lessons.objects.get(id=lessons_id)
    if delete_all:
        parent = lessons.parent
        Lessons.objects.filter(parent=parent).delete()
        parent.delete()
    else:
        lessons.delete()


def edit_lessons_from_form(form: EditLessonsForm, lessons_id: int):
    data = convert_cleaned_data_to_objects(form.cleaned_data)
    lessons = Lessons.objects.filter(id=lessons_id).first()
    parent = lessons.parent

    def _lessons_filter_fields() -> dict:
        available_fields = [
            'classroom', 'date', 'time_start', 'time_end', 'lessons_type',
            'subject', 'teacher', 'student', 'group',
        ]
        data['date'] = data['date_from_valid']
        data['time_end'] = calculate_time_end(
            data['time_start'],
            data['subject']
        )
        return {
            k: v for k, v in data.items() if k in available_fields
        }

    def _parent_filter_fields() -> dict:
        available_fields = ['date_from_valid', 'date_valid_until',
                            'weekdays_for_repeating']
        return {
            k: v for k, v in data.items() if k in available_fields
        }
    if lessons.parent and lessons.parent.count_of_children == 1:
        data['change_all'] = True

    if data.get('change_all'):
        if parent:
            Lessons.objects.filter(
                parent=lessons.parent,
                date__gt=now().date(),
            ).delete()
            parent.delete()
        else:
            lessons.delete()
        add_lessons_from_form(form)
    else:
        old_parent = parent
        parent = LessonsParent(**_parent_filter_fields())
        parent.save()

        update_data = dict(parent=parent)
        update_data.update(**_lessons_filter_fields())
        Lessons.objects.filter(id=lessons_id).update(**update_data)

        if old_parent and old_parent.count_of_children == 0:
            old_parent.delete()


def _group_lessons_by_classrooms(
    lessons: List[Lessons],
    classrooms: List[ClassRoom],
) -> dict:
    result = {}
    for cl in classrooms:
        data = list(filter(lambda x: x.classroom == cl, lessons))
        if data:
            result[cl.id] = data
    return result


def get_lessons_data_by_filter_form(form: FilterLessonsForm):
    add_days = form.cleaned_data['additional_days']
    dt_list = get_days_from_date(
        form.cleaned_data['date_from'],
        int(add_days if add_days else 7),
    )
    result = []
    classrooms = ClassRoom.objects.all()
    query_filter = {}
    if form.cleaned_data['classrooms']:
        objs = [
            ClassRoom.objects.get(id=int(v))
            for v in form.cleaned_data['classrooms']
        ]
        query_filter.update(classroom__in=objs)
    if form.cleaned_data['teachers']:
        objs = [
            Teacher.objects.get(id=int(v))
            for v in
            form.cleaned_data['teachers']
        ]
        query_filter.update(teacher__in=objs)
    if form.cleaned_data['students']:
        objs = [
            Student.objects.get(id=int(v))
            for v in
            form.cleaned_data['students']
        ]
        query_filter.update(student__in=objs)
    if form.cleaned_data['groups']:
        objs = [
            Group.objects.get(id=int(v))
            for v in
            form.cleaned_data['groups']
        ]
        query_filter.update(group__in=objs)
    if form.cleaned_data['types']:
        ids = [int(v) for v in form.cleaned_data['types']]
        query_filter.update(lessons_type__in=ids)

    for dt in dt_list:
        query_filter.update(date=dt)
        q = Lessons.objects.filter(**query_filter).order_by('time_start')
        data = _group_lessons_by_classrooms(q.all(), classrooms)
        cls_rms = list(filter(lambda x: x.id in data.keys(), classrooms))
        result.append((
            dt,
            get_weekday_name_by_date(dt),
            tuple(zip(cls_rms, data.values()))
        ))
    return result


def get_lessons_data_for_teachers(dt: date) -> Generator:
    for teacher in Teacher.objects.filter(status=STATUS_TEACHER_ACTIVE).all():
        lessons = Lessons.objects.filter(
            teacher=teacher,
            date=dt,
        ).order_by('time_start').all()
        lessons = fill_daily_lessons(lessons)
        yield LessonsScheduleTeachers(
            lessons=lessons,
            teacher=teacher,
            date=dt,
        )


def fill_daily_lessons(
    lessons: list[Lessons],
) -> list[Lessons]:
    time_periods = get_day_time_periods()
    existed_lessons = set()
    result = []
    i = 0
    for t in time_periods:
        i +=1
        res = list(filter(lambda l: l.time_start <= t < l.time_end, lessons))
        if len(res) > 0:
            r = res[0]
            print(i, t, r)
            if r.id not in existed_lessons:
                existed_lessons.add(r.id)
                result.append(r)
        else:
            result.append(EmptyLessons(t))

    return result
