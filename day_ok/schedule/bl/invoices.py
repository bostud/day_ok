from typing import List, Optional
from django.http import HttpRequest
from datetime import date
from ..models import (
    Invoice, Student, Service,
    InvoiceStatusChangeLog,
    InvoicePayment,
)
from django.db import transaction

OFFSET = 15


def get_invoices_per_page(page: int = 0) -> List[Invoice]:
    start = OFFSET * page
    end = OFFSET * (page + 1)
    return Invoice.objects.all().order_by('-date_created')[start: end]


def total_pages() -> range:
    return range(int(Invoice.objects.count() / OFFSET + 1))


def get_all_invoices() -> List[Invoice]:
    return Invoice.objects.all().order_by('-date_created')


def filter_invoices(
    students: Optional[List[int]] = None,
    services: Optional[List[int]] = None,
    subjects: Optional[List[int]] = None,
    statuses: Optional[List[int]] = None,
    service_types: Optional[List[int]] = None,
    date_valid_from: Optional[date] = None,
    date_valid_until: Optional[date] = None,
) -> List[Invoice]:
    query_filter = {}
    if students:
        query_filter.update(student_id__in=students)
    if services:
        query_filter.update(service_id__in=services)
    if date_valid_from:
        query_filter.update(date_valid_from__gte=date_valid_from)
    if date_valid_until:
        query_filter.update(date_valid_until__lte=date_valid_until)
    if statuses:
        query_filter.update(status__in=statuses)
    if service_types:
        query_filter.update(service__type_of__in=service_types)
    if subjects:
        query_filter.update(service__subject__in=subjects)
    return Invoice.objects.filter(**query_filter).order_by('-date_created')


@transaction.atomic
def create_invoice(
    request: HttpRequest,
    student: int,
    service: int,
    status: int,
    date_paid_until: date,
    date_valid_from: date,
    date_valid_until: date,
    payment_type: int = None,
    amount: int = None
) -> Optional[Invoice]:
    assert int(status) in Invoice.Status.values
    status = int(status)
    service = Service.objects.get(id=service)
    invoice = Invoice(
        student=Student.objects.get(id=student),
        service=service,
        status=status,
        date_valid_until=date_valid_until,
        date_valid_from=date_valid_from,
        date_paid_until=date_paid_until,
    )

    invoice.save()
    create_invoice_change_log(
        invoice=invoice,
        request=request,
        new_status=status,
        comment='Створення рахунку',
    )
    if payment_type:
        payment_type = int(payment_type)
    if amount:
        amount = int(amount)

    if status == Invoice.Status.PAID:
        create_invoice_payment(
            request, invoice, payment_type, service.price,
        )
    elif status == Invoice.Status.PENDING and amount and amount > 0:
        create_invoice_payment(
            request, invoice, payment_type, amount,
        )

    return invoice


@transaction.atomic
def create_invoice_payment(
    request: HttpRequest,
    invoice: Invoice,
    payment_type: int,
    amount: int,
    **kwargs,
) -> List[InvoicePayment]:
    if (
        not payment_type or
        payment_type not in InvoicePayment.PaymentType.values
    ):
        payment_type = InvoicePayment.PaymentType.CASH
    payment = InvoicePayment.objects.create(
        invoice=invoice,
        payment_type=payment_type,
        amount=amount,
    )

    create_invoice_change_log(
        invoice=invoice,
        request=request,
        new_status=invoice.status,
        previous_status=invoice.status,
        comment=f'Додавання оплати {payment.amount}грн.'
    )

    if invoice.amount_to_full_payment <= 0:
        prev_status = invoice.status
        invoice.status = Invoice.Status.PAID
        invoice.save()

        create_invoice_change_log(
            invoice=invoice,
            request=request,
            new_status=invoice.status,
            previous_status=prev_status,
            comment='Автоматично змінено на Оплачено'
        )

    return invoice.payments


def create_invoice_change_log(
    invoice: Invoice,
    request: HttpRequest,
    new_status: int,
    previous_status: Optional[int] = None,
    comment: Optional[str] = None,
):
    change_log = InvoiceStatusChangeLog(
        invoice=invoice,
        user=request.user,
        new_status=new_status,
        previous_status=previous_status,
        comment=comment,
    )
    change_log.save()
    return change_log


def get_invoice_change_log(
    invoice: Invoice,
) -> Optional[List[InvoiceStatusChangeLog]]:
    return InvoiceStatusChangeLog.objects.filter(
        invoice=invoice,
    ).order_by(
        '-datetime_created'
    ).all()


def get_invoice(id_: int) -> Optional[Invoice]:
    return Invoice.objects.filter(id=id_).first()


@transaction.atomic
def change_invoice_status(
    request: HttpRequest,
    invoice: Invoice,
    new_status: int,
) -> Invoice:
    assert int(new_status) in Invoice.Status.values
    if invoice.status != int(new_status):
        create_invoice_change_log(
            invoice=invoice,
            request=request,
            new_status=int(new_status),
            previous_status=invoice.status,
            comment='Зміна статусу',
        )
        invoice.status = int(new_status)
        invoice.save()

        if invoice.status == Invoice.Status.PAID:
            payments_sum = sum([i.amount for i in invoice.payments])
            if invoice.service.price > payments_sum:
                create_invoice_payment(
                    request=request,
                    invoice=invoice,
                    payment_type=InvoicePayment.PaymentType.CASH,
                    amount=invoice.service.price - payments_sum,
                )
                create_invoice_change_log(
                    invoice=invoice,
                    request=request,
                    new_status=invoice.status,
                    previous_status=invoice.status,
                    comment='Додано повну оплату',
                )

    return invoice


@transaction.atomic
def delete_invoice_payment(
    request: HttpRequest,
    payment_id: int
) -> Optional[Invoice]:
    payment = InvoicePayment.objects.filter(id=payment_id).first()
    if payment:
        invoice_id = payment.invoice.id
        invoice = Invoice.objects.get(id=invoice_id)
        create_invoice_change_log(
            invoice=invoice,
            request=request,
            new_status=Invoice.Status.PENDING,
            previous_status=invoice.status,
            comment=f'Видалення оплати {payment.amount}грн.'
        )
        invoice.status = Invoice.Status.PENDING
        invoice.save()
        payment.delete()
        return invoice
    return None


@transaction.atomic
def delete_invoice(
    request: HttpRequest,
    invoice: Invoice,
):
    create_invoice_change_log(
        invoice,
        request,
        invoice.status,
        invoice.status,
        'Видалення рахунку'
    )
    invoice.delete()
