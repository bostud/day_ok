from django import forms
from ..models import Subject


class SubjectForm(forms.Form):
    name = forms.CharField(
        min_length=1
    )
    hour = forms.IntegerField(min_value=1, max_value=4)
    minute = forms.IntegerField(min_value=0, max_value=59)

    name.widget.attrs.update({
        'class': 'form-control',
    })
    hour.widget.attrs.update({
        'type': 'number',
        'class': 'form-control',
        'placeholder': 'Год.',
        'title': 'Год.'
    })
    minute.widget.attrs.update({
        'type': 'number',
        'class': 'form-control',
        'placeholder': 'Хв.',
        'title': 'Хв.'
    })

    class Meta:
        model = Subject
        fields = ['name', 'duration']
