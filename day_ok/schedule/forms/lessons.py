from ..models import (
    ClassRoom, Subject, Lessons,
    Teacher, Student, Group,
)
from django import forms
from ..utils import get_weekdays_tuple, datetime_now_tz as now
from .utils import (
    get_groups, get_teachers, get_classrooms,
    DateInput, get_students, get_subjects, DateInputEmpty
)


def convert_cleaned_data_to_objects(form_cleaned_data: dict) -> dict:
    fcd = form_cleaned_data
    _converting_settings = (
        ('classroom', ClassRoom, int, None),
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
    classroom = forms.ChoiceField(
        label='Виберіть аудиторію',
        choices=get_classrooms,
    )

    date_from = forms.DateField(
        label='Виберіть дату',
        widget=DateInput(),
        help_text='* Буде показано 7 днів після вибраної дати',
        input_formats=['%d.%m.%Y'],
    )
    classroom.widget.attrs.update({'class': 'form-control'})


class LessonsByDayForm(forms.Form):
    date = forms.DateField(
        label='Виберіть дату для показу занять',
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
    )


class AddLessonsForm(forms.Form):
    classroom = forms.ChoiceField(
        label='Аудиторія',
        choices=get_classrooms,
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
        choices=Lessons.Type.choices,
        initial=Lessons.Type.INDIVIDUAL,
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
    classrooms = forms.MultipleChoiceField(
        label='Аудиторія:',
        choices=get_classrooms,
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
        choices=Lessons.Type.choices,
        required=False,
    )
    additional_days = forms.IntegerField(
        label='Період',
        required=False,
        initial=7,
        min_value=0,
        max_value=7,
    )

    classrooms.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
    teachers.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
    students.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
    groups.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
    additional_days.widget.attrs.update({
        'class': 'form-control',
    })
    types.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
