from django import forms
from .utils import DateInputEmpty, get_students, get_groups
from ..models import Lessons


class FilterPresenceForm(forms.Form):
    date_from = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        required=False,
    )
    students = forms.MultipleChoiceField(
        label='Учень:',
        choices=get_students,
        required=False,
    )
    groups = forms.MultipleChoiceField(
        choices=get_groups,
        required=False,
    )
    lessons_types = forms.MultipleChoiceField(
        choices=Lessons.Type.choices,
        required=False,
    )
    date_until = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        required=False,
    )

    page = forms.IntegerField(initial=1, required=False)
    per_page = forms.IntegerField(initial=10, required=False)

    students.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Студенти',
    })

    groups.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Групи',
    })

    lessons_types.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Тип заняття',
    })


class PresenceEditForm(forms.Form):
    students = forms.MultipleChoiceField()


class PresenceDeleteForm(forms.Form):
    student = forms.IntegerField(
        widget=forms.HiddenInput(),
    )
