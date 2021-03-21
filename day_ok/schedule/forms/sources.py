from django import forms
from .utils import get_free_source_students, get_sources
from ..models import Source
from ..bl.students import get_student

METHOD_DELETE = 'delete'
METHOD_EDIT = 'edit'
AVAILABLE_METHODS = [
   METHOD_DELETE,
   METHOD_EDIT,
]


class AddSource(forms.Form):
    name = forms.CharField(
        required=True,
        min_length=1,
    )

    name.widget.attrs.update({
        'class': 'form-control',
    })


def validate_delete_method(value: str) -> bool:
    return value == METHOD_DELETE


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


def validate_source_name(value: str) -> bool:
    return Source.objects.filter(name=value.strip()).count() == 0


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
