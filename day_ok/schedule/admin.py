from django.contrib import admin
from django.utils.timezone import now
# Register your models here.
from .models import (
    ClassRoom, Service, Teacher, Group, Student, Subject, Invoice, Lessons,
    Source, INVOICE_STATUSES, INVOICE_RECEIVERS
)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'lessons_count',
        'price',
        'currency',
    )

    list_editable = (
        'price',
        'lessons_count',
    )


class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'status',
    )

    list_editable = (
        'status',
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'status',
        'source',
    )

    list_editable = (
        'status',
    )

    list_per_page = 20


class ClassRoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'places_count',
        'room_type',
    )


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subject',
        'age_from',
        'teacher',
        'students_count',
    )


class LessonsAdmin(admin.ModelAdmin):
    list_display = (
        'class_room',
        'format_date',
        'format_time_start',
        'format_time_end',
        'lessons_type',
        'subject',
        'teacher',
        'duration',
    )

    list_per_page = 20


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'lessons_duration'
    )


class InvoiceStatusFilter(admin.SimpleListFilter):
    title = 'Статус рахунку'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return INVOICE_STATUSES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class InvoiceReceiverFilter(admin.SimpleListFilter):
    title = 'Отримувач'
    parameter_name = 'receiver'

    def lookups(self, request, model_admin):
        return INVOICE_RECEIVERS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(receiver=self.value())
        return queryset


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'student',
        'service',
        'receiver',
        'receiver_teacher',
        'format_date_created',
        'format_date_when_should_pay',
        'status',
        'days_left_for_payment',
        'status_payed',
    )

    search_fields = ('^student', '^status', '^service',)
    list_filter = (
        InvoiceStatusFilter,
        InvoiceReceiverFilter,
    )
    readonly_fields = ('number', )
    list_per_page = 10
    list_editable = ('status', )

    def format_date_created(self, rec: Invoice):
        return rec.date_created.strftime('%d.%m.%Y')

    def format_date_when_should_pay(self, rec: Invoice):
        return rec.date_when_should_pay.strftime('%d.%m.%Y')

    def days_left_for_payment(self, rec: Invoice) -> int:
        if rec.status == '2':
            return (rec.date_when_should_pay - now().date()).days
        return 0

    format_date_created.short_description = 'Дата створення'
    format_date_when_should_pay.short_description = (
        'Дата до якої здійснити оплату'
    )

    def status_payed(self, res: Invoice) -> bool:
        return res.status != '2'

    status_payed.boolean = True
    status_payed.short_description = 'Оплата'

    days_left_for_payment.short_description = 'Днів до оплати'


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'students_from_source_total',
    )


admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Lessons, LessonsAdmin)
admin.site.register(Source, SourceAdmin)
