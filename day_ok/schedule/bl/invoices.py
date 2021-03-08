from typing import List, Optional
from django.http import HttpRequest
from datetime import date
from ..models import Invoice, Student, Service, InvoiceStatusChangeLog

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
    return Invoice.objects.filter(**query_filter).order_by('-date_created')


def create_invoice(
    request: HttpRequest,
    student: int,
    service: int,
    status: int,
    date_paid_until: date,
    date_valid_from: date,
    date_valid_until: date,
) -> Optional[Invoice]:
    assert int(status) in Invoice.Status.values
    invoice = Invoice(
        student=Student.objects.get(id=student),
        service=Service.objects.get(id=service),
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
    )
    return invoice


def create_invoice_change_log(
    invoice: Invoice,
    request: HttpRequest,
    new_status: int,
    previous_status: Optional[int] = None,
):
    change_log = InvoiceStatusChangeLog(
        invoice=invoice,
        user=request.user,
        new_status=new_status,
        previous_status=previous_status,
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
            previous_status=invoice.status
        )
        invoice.status = int(new_status)
        invoice.save()

    return invoice
