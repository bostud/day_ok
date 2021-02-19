import logging
from datetime import date, timedelta, datetime
from ..models import (
    Lessons, StudentPresence, INDIVIDUAL, LESSONS_TYPES,
    ClassRoom, Subject, Teacher, Student, Group, LessonsParent,
)
from ..utils import get_days_from_date, get_weekday_number
from ..forms import (
    get_students, get_weekdays_tuple, get_groups, get_subjects, get_teachers,
    get_class_rooms, AddLessonsForm, EditLessonsForm
)
from ..data_classes.lessons import AddLessonsDC, EditLessonsDC
log = logging.getLogger(__name__)


def get_weekly_class_room_lessons_by_classroom(
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


def prepare_add_lessons_form_data() -> dict:
    return AddLessonsDC(
        class_rooms=get_class_rooms(),
        teachers=get_teachers(),
        students=get_students(),
        groups=get_groups(),
        subjects=get_subjects(),
        weekdays=get_weekdays_tuple(),
        lessons_types=LESSONS_TYPES
    ).to_dict()


def prepare_edit_lessons_form_data(lessons_id: int) -> dict:
    lessons = Lessons.objects.get(id=lessons_id)
    if not lessons:
        return {}
    return EditLessonsDC(
        class_room=lessons.class_room.id,
        teacher=lessons.teacher.id,
        subject=lessons.subject.id,
        student=lessons.student.id,
        group=lessons.group,
        date_from_valid=lessons.date,
        date_until_valid=lessons.date,
        time_start=lessons.time_start,
        time_end=lessons.time_end,
        lessons_type=lessons.lessons_type,
        parent=lessons.parent.id,
        change_all=True,
        weekdays_for_repeating=lessons.parent.weekdays_list
    ).to_dict()


def add_lessons_from_form(form: AddLessonsForm) -> int:
    time_start = form.cleaned_data['time_start']
    subject = Subject.objects.get(id=int(form.cleaned_data['subject']))
    datetime_end = (datetime.combine(
        date.today(), time_start) + subject.lessons_duration)
    assert date.today().day == datetime_end.day

    date_until_valid = form.cleaned_data['date_until_valid']
    date_from_valid = form.cleaned_data['date_from_valid']
    weekdays = [int(n) for n in form.cleaned_data['weekdays_for_repeating']]
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
    date_until_valid = date_until_valid or date_from_valid
    assert date_until_valid >= date_from_valid

    parent_lessons = LessonsParent()
    for i in range((date_until_valid - date_from_valid).days + 1):
        date_on = date_from_valid + timedelta(days=i)
        day_number = get_weekday_number(date_on)

        # пропуск дня, якщо він не у списку вибраних
        if weekdays and day_number not in weekdays:
            continue

        # add function - check if it free to create lessons
        parent_lessons.save()
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
            parent=parent_lessons,
        )
        ls.save()
        lessons_created += 1

    if lessons_created == 0:
        parent_lessons.delete()

    return lessons_created


def get_weekly_class_room_lessons_by_day(
    date_from: datetime,
) -> dict:
    result = {}
    classrooms = ClassRoom.objects.all()
    for clr in classrooms:
        lessons = Lessons.objects.filter(
            date=date_from,
            class_room__id=clr.id,
        ).order_by('time_start').all()
        for les in lessons:
            les.presence_count = (
                StudentPresence.objects.filter(lessons=les).count())
            if les.lessons_type == INDIVIDUAL:
                les.students_count = 1
            else:
                les.students_count = les.group.students.count()
        result[str(clr)] = list(lessons)

    return result


def delete_lessons(lessons_id: int, delete_all: bool):
    lessons = Lessons.objects.get(id=lessons_id)
    if delete_all:
        parent = lessons.parent
        for lsn in Lessons.objects.get(parent=parent):
            lsn.delete()
    else:
        lessons.delete()


def edit_lessons_from_form(form: EditLessonsForm, lessons_id: int):
    print(form.cleaned_data.items())
