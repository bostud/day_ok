from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from ..middleware import authenticated
from django.utils.timezone import now

from ..forms.invoices import (
    FilterInvoiceFrom, prepare_cleaned_data_to_form,
    CreateInvoiceForm, ChangeInvoiceStatusForm,
    AddPaymentForm, DeletePaymentForm,
)
from ..bl.invoices import (
    total_pages, filter_invoices, create_invoice,
    get_invoice_change_log, get_invoice, change_invoice_status,
    create_invoice_payment, delete_invoice, delete_invoice_payment
)


@authenticated
def invoices(request: HttpRequest, *args, **kwargs):
    page = request.GET.get('page', 0)
    if all([l.isdigit() for l in str(page)]):
        page = int(page)
    else:
        page = 0
    pages = total_pages()
    context = {
        'prev_page': page - 1,
        'pages': total_pages(),
        'current_page': page,
        'next_page': page + 1 if page + 1 < max(pages) else page,
        'create_form': CreateInvoiceForm(),
        'payment_form': AddPaymentForm(),
    }
    form = FilterInvoiceFrom(request.GET)
    if form.is_valid():
        form_data = prepare_cleaned_data_to_form(form)
        context.update(filter_form=FilterInvoiceFrom(
            form_data
        ))
        context.update(invoices=filter_invoices(**form.cleaned_data))
    else:
        context.update(filter_form=FilterInvoiceFrom({
            'date_valid_from': now().strftime('%d.%m.%Y')
        }))
        context.update(invoices=filter_invoices(date_valid_from=now().date()))

    return render(request, 'schedule/invoices/base.html', context)


@authenticated
def invoices_add(request: HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = CreateInvoiceForm(request.POST)
        if form.is_valid():
            create_invoice(request, **form.cleaned_data)
    return HttpResponseRedirect('/schedule/invoices')


@authenticated
def invoices_actions(request: HttpRequest, action: str, invoice_id: int):

    context: Dict[Any, Any] = {}
    errors = []

    def __error_wrong_action():
        return f'Невірна дія над рахунком: {action} - {invoice_id}'

    def __error_not_found():
        return f'Рахунок не знайдено: {invoice_id}'

    def trow_errors(*errors):
        context.update(errors=[*errors])
        return render(request, 'schedule/invoices/base.html', context)

    invoice = get_invoice(int(invoice_id))
    if not invoice:
        errors.append(__error_not_found())
        trow_errors()

    def _view():
        change_log = get_invoice_change_log(invoice)
        context.update(invoice=invoice)
        context.update(history_records=change_log)
        context.update(change_status_form=ChangeInvoiceStatusForm())
        context.update(payment_form=AddPaymentForm({
            'amount': invoice.amount_to_full_payment,
            'redirect_to': '',
        }))
        return render(request, 'schedule/invoices/view.html', context)

    def _paid():
        from ..models import Invoice
        if request.method == 'POST':
            invoice = get_invoice(int(invoice_id))
            if invoice:
                change_invoice_status(
                    request,
                    invoice,
                    new_status=Invoice.Status.PAID,
                )
        return HttpResponseRedirect('/schedule/invoices')

    def _add_payment():
        if request.method == 'POST':
            form = AddPaymentForm(request.POST)
            if form.is_valid():
                create_invoice_payment(request, invoice, **form.cleaned_data)

                if form.cleaned_data['redirect_to'] == 'invoices':
                    return HttpResponseRedirect(f'/schedule/invoices')
        return HttpResponseRedirect(f'/schedule/invoices/view/{invoice_id}')

    def _delete_payment():
        if request.method == 'POST':
            form = DeletePaymentForm(request.POST)
            if form.is_valid():
                delete_invoice_payment(request, **form.cleaned_data)
        return HttpResponseRedirect(f'/schedule/invoices/view/{invoice_id}')

    def _delete():
        if request.method == 'POST':
            delete_invoice(request, invoice)
        return HttpResponseRedirect(f'/schedule/invoices')

    _actions = {
        'view': _view,
        'paid': _paid,
        'add_payment': _add_payment,
        'delete_payment': _delete_payment,
        'delete': _delete,
    }

    if action not in _actions:
        trow_errors(__error_wrong_action())

    res = _actions[action]()
    if res:
        return res

    context.update(errors=errors)
    context.update(invoices=filter_invoices())
    context.update(info_posts=['Сервіс на епаті розробки, натисніть "Очистити"'])
    return render(request, 'schedule/invoices/base.html', context)


@authenticated
def invoices_change_status(request: HttpRequest, invoice_id: int):
    if request.method == 'POST':
        form = ChangeInvoiceStatusForm(request.POST)
        if form.is_valid():
            invoice = get_invoice(int(invoice_id))
            if invoice:
                change_invoice_status(
                    request=request,
                    invoice=invoice,
                    new_status=form.cleaned_data['status']
                )
                return HttpResponseRedirect(
                    f'/schedule/invoices/view/{invoice_id}'
                )
    return HttpResponseRedirect('/schedule/invoices')
