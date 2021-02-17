from .models import (
    ClassRoom, Subject, LESSONS_TYPES,
    Teacher, STATUS_TEACHER_ACTIVE,
    Student, Group, STATUS_STUDENT_ACTIVE,
)
from django import forms
from functools import partial
from .utils import get_weekdays_tuple
DateInput = partial(forms.DateInput, {'class': 'datepicker form-control'})


def get_class_rooms() -> list:
    cl_r = ClassRoom.objects.all()
    res = []
    for room in cl_r:
        res.append((room.id, str(room)))
    return res


def get_subjects() -> list:
    iter_ = Subject.objects.all()
    res = []
    for i in iter_:
        res.append((i.id, str(i.name)))
    return res


def get_teachers() -> list:
    iter_ = Teacher.objects.filter(status=STATUS_TEACHER_ACTIVE).all()
    res = []
    for i in iter_:
        if i.subjects:
            res.append((i.id, str(i)))
    return res


def get_students() -> list:
    iter_ = Student.objects.filter(status=STATUS_STUDENT_ACTIVE).all()
    res = []
    for i in iter_:
        res.append((i.id, str(i)))
    return res


def get_groups() -> list:
    iter_ = Group.objects.all()
    res = []
    for i in iter_:
        if i.students:
            res.append((i.id, str(i)))
    return res


class LessonsForm(forms.Form):
    class_room = forms.ChoiceField(
        label='Виберіть аудиторію',
        choices=get_class_rooms,
    )

    date_from = forms.DateField(
        label='Виберіть дату',
        widget=DateInput(),
        help_text='* Буде показано 7 днів після вибраної дати'
    )
    class_room.widget.attrs.update({'class': 'form-control'})


class EventsForm(LessonsForm):
    pass


class AddLessonsForm(forms.Form):
    class_room = forms.ChoiceField(
        label='Аудиторія',
        choices=get_class_rooms,
    )
    time_start = forms.TimeField(
        label='Початок заняття',
    )
    subject = forms.ChoiceField(
        label='Предмет',
        choices=get_subjects,
    )
    lessons_type = forms.ChoiceField(
        label='Тип заняття',
        choices=LESSONS_TYPES,
        initial=LESSONS_TYPES[0][0],
    )
    teacher = forms.ChoiceField(
        label='Викладач',
        choices=get_teachers,
    )
    student = forms.ChoiceField(
        label='Учень',
        help_text='Тільки якщо тип - індивідуальний',
        choices=get_students,
        initial='',
        required=False,
    )
    group = forms.ChoiceField(
        label='Група',
        help_text='Тільки якщо тип - груповий',
        choices=get_groups,
        initial='',
        required=False,
    )

    date_from_valid = forms.DateField(
        label='Вкажіть дату початку занять',
        help_text='',
        widget=DateInput(),
    )

    date_until_valid = forms.DateField(
        label='Вкажіть дату до якої створити заняття',
        help_text='',
        widget=DateInput(),
    )

    week_days_for_repeating = forms.MultipleChoiceField(
        label='Вкажіть дні тижня',
        choices=get_weekdays_tuple,
    )
