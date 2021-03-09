from django import forms
from datetime import date, timedelta
from ..models import Invoice, Service
from .utils import get_services, get_students, DateInputEmpty
from ..utils import datetime_now_tz as now, get_next_month_from_date


def get_first_date_of_month() -> str:
    dt = now()
    return date(dt.year, dt.month, 1).strftime('%d.%m.%Y')


def get_last_date_of_month() -> str:
    dt = now()
    next_month = get_next_month_from_date(dt)
    return (next_month - timedelta(days=1)).date().strftime('%d.%m.%Y')


def get_invoice_statuses() -> list:
    return Invoice.Status.choices


def get_service_types() -> list:
    return Service.TypeOf.choices


def prepare_cleaned_data_to_form(form: 'FilterInvoiceFrom') -> dict:
    res = {}
    fc = form.cleaned_data
    res.update(**fc)
    if res.get('date_valid_from'):
        res['date_valid_from'] = res['date_valid_from'].strftime('%d.%m.%Y')

    if res.get('date_valid_until'):
        res['date_valid_until'] = res['date_valid_until'].strftime('%d.%m.%Y')
    return res


class FilterInvoiceFrom(forms.Form):
    services = forms.MultipleChoiceField(
        choices=get_services,
        required=False,
    )

    students = forms.MultipleChoiceField(
        choices=get_students,
        required=False,
    )

    statuses = forms.MultipleChoiceField(
        choices=get_invoice_statuses,
        required=False,
    )

    service_types = forms.MultipleChoiceField(
        choices=get_service_types,
        required=False,
    )

    date_valid_from = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        required=False,
    )

    date_valid_until = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        required=False,
    )

    services.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Послуги',
    })

    students.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Учні',
    })

    statuses.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Статус',
    })

    service_types.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Тип послуги',
    })

    date_valid_from.widget.attrs.update({
        'placeholder': 'Дата з',
        'onChange': 'this.form.submit()',
    })

    date_valid_until.widget.attrs.update({
        'placeholder': 'Дата по',
        'onChange': 'this.form.submit()',
    })


class CreateInvoiceForm(forms.Form):
    student = forms.ChoiceField(
        choices=get_students,
        required=True,
    )
    service = forms.ChoiceField(
        choices=get_services,
        required=True,
    )

    date_paid_until = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
    )

    date_valid_from = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        initial=get_first_date_of_month,
    )

    date_valid_until = forms.DateField(
        widget=DateInputEmpty(),
        input_formats=['%d.%m.%Y'],
        initial=get_last_date_of_month,
    )

    status = forms.ChoiceField(
        choices=get_invoice_statuses,
        required=False,
    )

    service.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Послуга',
    })

    status.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Статус',
    })

    student.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Учень',
    })

    date_valid_until.widget.attrs.update({
        'placeholder': 'Дісний по',
    })

    date_valid_from.widget.attrs.update({
        'placeholder': 'Дісний з',
    })

    date_paid_until.widget.attrs.update({
        'placeholder': 'Оплатити до',
        'title': 'Оплатити до',
    })


class ChangeInvoiceStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=get_invoice_statuses,
    )

    status.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Новий статус',
    })
