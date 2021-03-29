from django.contrib import admin
from django.utils.timezone import now
# Register your models here.
from .models import (
    ClassRoom, Service, Teacher, Group, Student, Subject, Invoice, Lessons,
    Source, Event,
)


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


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subject',
        'age_from',
        'teacher',
        'students_count',
    )

    autocomplete_fields = ['students', 'teacher']

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


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lessons, LessonsAdmin)
