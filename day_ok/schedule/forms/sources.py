from django import forms
from .utils import get_free_source_students
from .validators import validate_delete_method, validate_source_name
from ..bl.students import get_student


class AddSource(forms.Form):
    name = forms.CharField(
        required=True,
        min_length=1,
    )

    name.widget.attrs.update({
        'class': 'form-control',
    })


class DeleteSourceForm(forms.Form):
    source = forms.IntegerField()
    method = forms.CharField(validators=[validate_delete_method])


class ConnectStudentsForm(forms.Form):
    students = forms.MultipleChoiceField(
        choices=get_free_source_students,
    )

    students.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })


class ChangeNameForm(forms.Form):
    name = forms.CharField(
        validators=[validate_source_name]
    )


def validate_student_exist(value: int) -> bool:
    student_id = int(value)
    return bool(get_student(student_id))


class DisconnectStudentForm(forms.Form):
    student = forms.IntegerField(
        validators=[validate_student_exist],
    )
    redirect_to = forms.CharField(
        required=False,
    )
