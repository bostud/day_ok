from django import forms
from ..utils import datetime_now_tz as now
from .utils import (
    DateInput, get_classrooms, get_students
)


class FilterEventsForm(forms.Form):
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
    students = forms.MultipleChoiceField(
        label='Учень:',
        choices=get_students,
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
    students.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
    additional_days.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
