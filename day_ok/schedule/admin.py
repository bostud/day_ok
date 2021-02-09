from django.contrib import admin

# Register your models here.
from .models import (
    ClassRoom, Service, Teacher, Group, Student, Subject, Invoice, Lessons,
    Source,
)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'lessons_count', 'price', 'currency')


class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'status',
    )


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


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'lessons_duration'
    )


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'student',
        'service',
        'receiver',
        'receiver_teacher',
        'date_created',
        'date_when_should_pay',
        'status',
    )


admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Lessons, LessonsAdmin)
admin.site.register(Source)
