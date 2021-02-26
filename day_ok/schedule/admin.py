from django.contrib import admin
from django.utils.timezone import now
# Register your models here.
from .models import (
    ClassRoom, Service, Teacher, Group, Student, Subject, Invoice, Lessons,
    Source, INVOICE_STATUSES, INVOICE_RECEIVERS, StudentPresence, Event,
)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'lessons_count',
        'price',
        'currency',
        'total_invoices',
        'payed_invoices',
    )

    search_fields = ['name']

    list_per_page = 10

    def total_invoices(self, rec: Service):
        return Invoice.objects.filter(service=rec).count()

    def payed_invoices(self, rec: Service):
        return Invoice.objects.filter(service=rec, status='1').count()

    total_invoices.short_description = 'Всього рахунків'
    payed_invoices.short_description = 'Оплачених рахунків'


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ['last_name', 'first_name']
    list_display = (
        'last_name',
        'first_name',
        'phone_number',
        'status',
        'count_of_subjects',
    )

    list_editable = (
        'status',
    )

    list_per_page = 10

    autocomplete_fields = ['subjects', ]

    def count_of_subjects(self, rec: Teacher):
        if rec.subjects:
            return rec.subjects.count()
        return 0

    count_of_subjects.short_description = 'К-сть предметів'


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['last_name', 'first_name']
    list_display = (
        'last_name',
        'first_name',
        'phone_number',
        'status',
        'source',
        'years_old',
    )

    readonly_fields = ('years_old', )

    list_editable = (
        'status',
    )

    list_per_page = 10

    def years_old(self, rec: Student):
        dt_birth = rec.date_of_birth
        if dt_birth:
            dt_now = now()
            years = dt_now.year - dt_birth.year
            if (
                dt_now.month >= dt_birth.month and
                dt_now.day >= dt_birth.day
            ):
                return years
            else:
                return years - 1
        return '---'

    years_old.short_description = 'Вік'


class ClassRoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'places_count',
        'room_type',
    )
    search_fields = ['name', ]


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subject',
        'age_from',
        'teacher',
        'students_count',
    )

    autocomplete_fields = ['students', 'teacher', 'subject']

    list_per_page = 10

    def students_count(self, rec: Group):
        return rec.students.count()

    students_count.short_description = 'К-сть учнів'


class LessonsAdmin(admin.ModelAdmin):
    list_display = (
        'classroom',
        'format_date',
        'format_time_start',
        'format_time_end',
        'lessons_type',
        'subject',
        'teacher',
        'duration',
    )

    fields = (
        ('classroom',), ('subject', 'teacher'),
        ('lessons_type', 'student', 'group'),
        ('date', 'time_start', 'time_end'),
    )

    readonly_fields = ['parent']

    list_per_page = 10


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'lessons_duration'
    )

    search_fields = ['name', ]


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

    autocomplete_fields = ['student', 'receiver_teacher', ]

    search_fields = (
        'student__last_name',
        'student__first_name',
        'status',
        'service__name',
    )
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

    def status_payed(self, res: Invoice) -> bool:
        return res.status != '2'

    status_payed.boolean = True
    status_payed.short_description = 'Оплата'
    format_date_created.short_description = 'Дата створення'
    format_date_when_should_pay.short_description = (
        'Дата до якої здійснити оплату'
    )
    days_left_for_payment.short_description = 'Днів до оплати'


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'students_from_source_total',
    )


class StudentPresenceAdmin(admin.ModelAdmin):
    list_display = (
        'lessons',
        'student',
        'is_presence',
        'date',
    )

    def date(self, rec: StudentPresence):
        return rec.lessons.date.strftime('%d.%m.%Y')

    date.short_description = 'Дата заняття'


class EventAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = (
        'name',
        'classroom',
        'date_of_event_formated',
        'time_start',
        'time_end',
        'count_of_participants',
    )
    autocomplete_fields = ['participants', 'classroom']

    def count_of_participants(self, rec: Event):
        return rec.participants.count()

    def date_of_event_formated(self, rec: Event):
        return rec.date_of_event.strftime('%d.%m.%Y')

    date_of_event_formated.short_description = 'Дата заходу'
    count_of_participants.short_description = 'К-сть учасників'

    list_per_page = 10


admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Lessons, LessonsAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(StudentPresence, StudentPresenceAdmin)
admin.site.register(Event, EventAdmin)
