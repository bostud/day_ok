from django import forms
from ..models import Invoice, Service, InvoicePayment
from .utils import (
    get_services, get_students,
    DateInputEmpty,
    get_subjects,
)
from ..utils import get_first_date_of_month, get_last_date_of_month


def get_invoice_statuses() -> list:
    return Invoice.Status.choices


def get_service_types() -> list:
    return Service.TypeOf.choices


def get_invoice_payment_types() -> list:
    return InvoicePayment.PaymentType.choices


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

    subjects = forms.MultipleChoiceField(
        choices=get_subjects,
        required=False,
    )

    services.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Послуги',
    })

    subjects.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'multiply': 'multiply',
        'data-selected-text-format': 'count',
        'title': 'Предмети',
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

    subject = forms.ChoiceField(
        choices=get_subjects,
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
    )

    payment_type = forms.ChoiceField(
        choices=get_invoice_payment_types,
        required=False,
    )

    amount = forms.IntegerField(
        min_value=0,
        required=False,
    )

    amount.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Сума',
    })

    service.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Послуга',
        'onchange': 'getSubjects(this)',
        'required': True,
    })

    subject.widget.attrs.update({
        'class': 'form-control',
        'title': 'Предмет',
        'hidden': True,
        'required': True,
    })

    status.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Статус',
        'onchange': 'shouldOpenPaymentType(this)',
        'required': True,
    })

    payment_type.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Тип оплати',
    })

    student.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Учень',
        'required': True,
    })

    date_valid_until.widget.attrs.update({
        'placeholder': 'Дісний по',
        'required': True,
    })

    date_valid_from.widget.attrs.update({
        'placeholder': 'Дісний з',
        'required': True,
    })

    date_paid_until.widget.attrs.update({
        'placeholder': 'Оплатити до',
        'title': 'Оплатити до',
        'required': True,
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


class AddPaymentForm(forms.Form):
    payment_type = forms.ChoiceField(
        choices=get_invoice_payment_types,
        required=False,
    )

    amount = forms.IntegerField(
        min_value=1,
    )

    redirect_to = forms.CharField(
        required=False,
        initial='invoices',
    )

    payment_type.widget.attrs.update({
        'class': 'form-control selectpicker',
        'data-live-search': 'true',
        'title': 'Спосіб оплати',
    })

    amount.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Сума',
    })

    redirect_to.widget.attrs.update({
        'hidden': True,
    })


class DeletePaymentForm(forms.Form):
    payment_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
