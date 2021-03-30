from django import forms
from ..models import Group
from .utils import get_subjects, get_teachers, get_students
from .validators import validate_group_name


class GroupForm(forms.Form):
    name = forms.CharField(
        min_length=1,
        validators=[
            validate_group_name,
        ],
    )
    subject = forms.ChoiceField(
        choices=get_subjects,
    )
    age_from = forms.IntegerField()
    teacher = forms.ChoiceField(
        choices=get_teachers,
    )
    students = forms.MultipleChoiceField(
        required=False,
        choices=get_students,
    )

    name.widget.attrs.update({
        'class': 'form-control',
    })
    age_from.widget.attrs.update({
        'class': 'form-control',
    })
    students.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
    teacher.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
    })
    subject.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
    })

    class Meta:
        model = Group
        fields = ['name', 'subject', 'students', 'teacher', 'age_from']
