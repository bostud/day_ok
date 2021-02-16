from .models import ClassRoom, Lessons
from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': ''})


def get_class_rooms() -> list:
    res = []
    for room in ClassRoom.objects.all():
        res.append((room.id, str(room)))
    return res


class LessonsForm(forms.Form):
    class_room = forms.ChoiceField(
        label='Виберіть аудиторію',
        choices=get_class_rooms(),
    )

    date_from = forms.DateField(
        label='Виберіть дату',
        widget=DateInput(),
        help_text='* Буде показано 7 днів після вибраної дати'
    )
    class_room.widget.attrs.update({'class': 'form-control'})
    date_from.widget.attrs.update({'class': 'datepicker form-control'})
