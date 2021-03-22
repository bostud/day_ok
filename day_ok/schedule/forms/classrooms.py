from django import forms
from .utils import get_classrooms_types
from .validators import validate_delete_method, validate_edit_method
from ..models import ClassRoom


class AddClassRoomForm(forms.Form):
    name = forms.CharField(
        min_length=1,
    )
    places_count = forms.IntegerField(
        required=False,
        initial=0,
    )
    room_type = forms.ChoiceField(
        choices=get_classrooms_types,
    )
    description = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        initial='',
    )

    room_type.widget.attrs.update({
        'class': 'form-control selectpicker',
    })

    places_count.widget.attrs.update({
        'class': 'form-control',
    })

    description.widget.attrs.update({
        'class': 'form-control',
        'rows': 5,
    })

    name.widget.attrs.update({
        'class': 'form-control',
    })

    class Meta:
        model = ClassRoom
        fields = ['name', 'places_count', 'room_type', 'description']


class DeleteClassRoomForm(forms.Form):
    classroom = forms.IntegerField()
