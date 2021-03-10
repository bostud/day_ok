from django import forms
from .utils import get_sources, DateTimeInput
from ..utils import datetime_now_tz as now
from ..models import Student


class AddStudentForm(forms.Form):
    first_name = forms.CharField(
        max_length=50
    )
    last_name = forms.CharField(
        max_length=50,
    )
    source = forms.ChoiceField(
        choices=get_sources,
    )
    date_test_lessons = forms.DateTimeField(
        label='Дата-час тестового заняття',
        widget=DateTimeInput(),
        input_formats=['%d.%m.%Y %H:%M'],
        initial=now,
    )
    date_start_studying = forms.DateTimeField(
        label='Дата старту навчання',
        widget=DateTimeInput(),
        input_formats=['%d.%m.%Y %H:%M'],
    )
    parent_phone = forms.CharField(
        max_length=50,
    )
    parent_first_name = forms.CharField(
        max_length=13,
    )
    parent_last_name = forms.CharField(
        max_length=100,
    )


class ChangeStudentStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=Student.Status.choices,
    )

    status.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Новий статус',
    })
