from django import forms
from .utils import DateInputEmpty
from ..utils import get_last_date_of_month, get_first_date_of_month


class TeacherSalaryStatForm(forms.Form):
    date_start = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        initial=get_first_date_of_month,
    )

    date_end = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        initial=get_last_date_of_month,
    )
    date_start.widget.attrs.update({
        'placeholder': 'Дата з',
        'onChange': 'this.form.submit()',
    })

    date_end.widget.attrs.update({
        'placeholder': 'Дата по',
        'onChange': 'this.form.submit()',
    })
