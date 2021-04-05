from django import forms
from ..models import Teacher
from .utils import get_subjects, DateInputEmpty


class TeacherLessonsColorForm(forms.Form):
    color = forms.CharField(max_length=10)
    font_color = forms.CharField(max_length=10)


class TeacherForm(forms.Form):
    first_name = forms.CharField(
        min_length=1,
        max_length=50,
    )
    last_name = forms.CharField(
        min_length=1,
        max_length=150,
    )
    phone_number = forms.CharField(
        min_length=1,
        max_length=13,
    )
    email = forms.CharField(
        min_length=1,
        max_length=150,
        required=False,
    )
    date_of_birth = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
    )
    date_start = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
    )
    subjects = forms.MultipleChoiceField(
        choices=get_subjects,
        required=False,
    )

    status = forms.ChoiceField(
        choices=Teacher.Status.choices,
        required=False,
    )

    first_name.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    phone_number.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    subjects.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })
    status.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Teacher
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',
            'date_of_birth', 'date_start', 'subjects', 'status',
        ]
