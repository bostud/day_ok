from .models import (
    ClassRoom, Subject, LESSONS_TYPES,
    Teacher, STATUS_TEACHER_ACTIVE,
    Student, Group, STATUS_STUDENT_ACTIVE,
)
from django import forms
from functools import partial
from .utils import get_weekdays_tuple
from django.utils.timezone import now
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


def convert_cleaned_data_to_objects(form_cleaned_data: dict) -> dict:
    fcd = form_cleaned_data
    _converting_settings = (
        ('class_room', ClassRoom, int, None),
        ('subject', Subject, int, None),
        ('teacher', Teacher, int, None),
        ('student', Student, int, None),
        ('group', Group, int, None),

    )

    result = {
        k: obj.objects.get(id=fmt(fcd[k])) if fcd.get(k) and fcd[k] else df
        for k, obj, fmt, df in _converting_settings
    }
    result.update(
        weekdays_for_repeating=[int(v) for v in fcd['weekdays_for_repeating']]
    )
    fcd.update(**result)
    return fcd


class LessonsByClassRoomForm(forms.Form):
    class_room = forms.ChoiceField(
        label='Виберіть аудиторію',
        choices=get_class_rooms,
    )

    date_from = forms.DateField(
        label='Виберіть дату',
        widget=DateInput(),
        help_text='* Буде показано 7 днів після вибраної дати',
        input_formats=['%d.%m.%Y'],
    )
    class_room.widget.attrs.update({'class': 'form-control'})


class EventsForm(LessonsByClassRoomForm):
    pass


class LessonsByDayForm(forms.Form):
    date = forms.DateField(
        label='Виберіть дату для показу занять',
        widget=DateInput(),
        input_formats=['%d.%m.%Y'],
    )


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
        input_formats=['%d.%m.%Y'],
    )

    date_until_valid = forms.DateField(
        label='Вкажіть дату до якої створити заняття',
        help_text='',
        widget=DateInput(),
        input_formats=['%d.%m.%Y'],
        required=False,
    )

    weekdays_for_repeating = forms.MultipleChoiceField(
        label='Вкажіть дні тижня',
        choices=get_weekdays_tuple,
        required=False,
    )


class EditLessonsForm(AddLessonsForm):
    change_all = forms.BooleanField(
        required=False,
        initial=False,
    )


class FilterLessonsForm(forms.Form):
    date_from = forms.DateField(
        label='Дата',
        help_text='',
        widget=DateInput(),
        input_formats=['%d.%m.%Y'],
        initial=now,
    )
    class_rooms = forms.MultipleChoiceField(
        label='Аудиторія:',
        choices=get_class_rooms,
        required=False,
    )
    teachers = forms.MultipleChoiceField(
        label='Викладач:',
        choices=get_teachers,
        required=False,
    )
    students = forms.MultipleChoiceField(
        label='Учень:',
        choices=get_students,
        required=False,
    )
    groups = forms.MultipleChoiceField(
        label='Група',
        choices=get_groups,
        required=False,
    )
    types = forms.MultipleChoiceField(
        label='Типи',
        choices=LESSONS_TYPES,
        required=False,
    )
    additional_days = forms.IntegerField(
        label='Період',
        required=False,
        initial=7,
        min_value=0,
        max_value=7,
    )

    class_rooms.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })
    teachers.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })
    students.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })
    groups.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })
    additional_days.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })
    types.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })
