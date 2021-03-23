from django import forms
from .utils import get_service_type_of, get_subjects
from ..models import Service


class GetServiceSubjectsForm(forms.Form):
    service = forms.IntegerField()


class ServiceForm(forms.Form):
    name = forms.CharField(
        min_length=1,
    )
    type_of = forms.ChoiceField(
        choices=get_service_type_of,
    )
    subjects = forms.MultipleChoiceField(
        choices=get_subjects,
        required=False,
    )
    price = forms.IntegerField()
    lessons_count = forms.IntegerField()

    name.widget.attrs.update({
        'class': 'form-control',
    })

    type_of.widget.attrs.update({
        'class': 'form-control selectpicker',
    })

    price.widget.attrs.update({
        'class': 'form-control',
    })

    lessons_count.widget.attrs.update({
        'class': 'form-control',
    })

    subjects.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
    })

    class Meta:
        models = Service
        fields = ['name', 'type_of', 'subjects', 'lessons_count', 'price']


class DeleteSubjectFromServiceForm(forms.Form):
    subject = forms.IntegerField()
