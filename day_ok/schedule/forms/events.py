from django import forms
from .utils import (
    DateInputEmpty, get_students,
    get_event_locations,
)
from ..models import EventLocation, Event


class FilterEventsForm(forms.Form):
    date_from = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        required=False,
    )
    location = forms.MultipleChoiceField(
        label='Локація:',
        choices=get_event_locations,
        required=False,
    )
    student = forms.MultipleChoiceField(
        label='Учень:',
        choices=get_students,
        required=False,
    )
    date_until = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        required=False,
    )

    location.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })
    student.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })


class EventForm(forms.Form):
    name = forms.CharField(
        min_length=1
    )
    date_of_event = forms.DateField(
        label='Дата',
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
    )
    time_start = forms.TimeField(
        required=False,
    )
    time_end = forms.TimeField(
        required=False,
    )
    location = forms.ChoiceField(
        choices=get_event_locations,
    )
    participants = forms.MultipleChoiceField(
        choices=get_students,
    )

    name.widget.attrs.update({
        'class': 'form-control',
    })

    time_start.widget.attrs.update({
        'class': 'form-control',
    })

    time_end.widget.attrs.update({
        'class': 'form-control',
        'type': 'time'
    })

    location.widget.attrs.update({
        'class': 'form-control selectpicker',
    })

    participants.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
    })

    class Meta:
        models = Event
        fields = [
            'name', 'date_of_event', 'time_start',
            'time_end', 'location', 'participants'
        ]


class EventLocationForm(forms.Form):
    location = forms.CharField(
        min_length=1
    )

    location.widget.attrs.update({
        'class': 'form-control',
    })

    class Meta:
        model = EventLocation
        fields = ['location']


class EventParticipantDeleteForm(forms.Form):
    participant = forms.IntegerField()
