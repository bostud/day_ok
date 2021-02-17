import logging
from datetime import date, timedelta, datetime
from ..models import (
    Lessons, StudentPresence, INDIVIDUAL, LESSONS_TYPES,
    ClassRoom, Subject, Teacher, Student, Group
)
from ..utils import get_days_from_date, get_weekday_number
from ..forms import (
    get_students, get_weekdays_tuple, get_groups, get_subjects, get_teachers,
    get_class_rooms, AddLessonsForm,
)

log = logging.getLogger(__name__)


def get_weekly_class_room_lessons_by_day(
    class_room_id: int,
    date_from: date,
) -> dict:
    result = {}
    days = get_days_from_date(date_from)
    for d in days:
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


def prepare_add_lessons_landing_data() -> dict:
    return {
        'class_rooms': get_class_rooms(),
        'teachers': get_teachers(),
        'students': get_students(),
        'groups': get_groups(),
        'subjects': get_subjects(),
        'weekdays': get_weekdays_tuple(),
        'lessons_types': LESSONS_TYPES,
    }


def add_lessons_from_form(form: AddLessonsForm) -> int:
    date_until_valid = form.cleaned_data['date_until_valid']
    time_start = form.cleaned_data['time_start']
    subject = Subject.objects.get(id=int(form.cleaned_data['subject']))
    datetime_end = (datetime.combine(
        date.today(), time_start) + subject.lessons_duration)
    assert date.today().day == datetime_end.day

    date_from_valid = form.cleaned_data['date_from_valid']
    weekdays = [int(n) for n in form.cleaned_data['week_days_for_repeating']]
    class_room = ClassRoom.objects.get(id=int(form.cleaned_data['class_room']))

    teacher = Teacher.objects.get(id=int(form.cleaned_data['teacher']))
    lessons_type = form.cleaned_data['lessons_type']
    if lessons_type == INDIVIDUAL:
        student = Student.objects.get(id=int(form.cleaned_data['student']))
        group = None
    else:
        student = None
        group = Group.objects.get(id=int(form.cleaned_data['group']))

    time_end = datetime_end.time()

    lessons_created = 0
    for i in range((date_until_valid - date_from_valid).days + 1):
        date_on = date_from_valid + timedelta(days=i)
        day_number = get_weekday_number(date_on)
        if day_number in weekdays:
            # add function - check if it free to create lessons
            ls = Lessons(
                class_room=class_room,
                date=date_on,
                time_start=time_start,
                time_end=time_end,
                lessons_type=lessons_type,
                subject=subject,
                group=group,
                student=student,
                teacher=teacher,
            )
            ls.save()
            lessons_created += 1

    return lessons_created
