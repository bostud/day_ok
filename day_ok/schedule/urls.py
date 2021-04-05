from django.urls import path
from .views import (
    home_view,
    reports,
    lessons_view, lessons_actions, add_lessons,
    events, event_actions, event_location,
    classrooms, classrooms_actions,
    groups, groups_actions, group_delete, group_unpin_student,
    students_actions, students,
    teachers, teachers_view, set_teacher_lessons_style, teacher_delete,
    unpin_subject,
    invoices, invoices_actions,
    invoices_add, invoices_change_status,
    finance, get_service_subjects,
    sources, source_actions, source_actions_view,
    services, services_actions,
    presence, present_actions,
    subject, subject_view, subject_delete,
)

lessons_urlpatterns = [
    path('lessons/add/', add_lessons, name='add_lessons'),
    path('lessons/show_by/<str:show_type>/', lessons_view, name='lessons'),
    path(
        'lessons/<str:action>/<int:lessons_id>/',
        lessons_actions,
        name='lessons_action',
    ),
]

event_urlpatterns = [
    path('events', events, name='events'),
    path(
        'event/<int:event_id>/<str:action>/',
        event_actions,
        name='event_actions',
    ),
    path('event_location', event_location, name='event_location'),
]

classrooms_urlpatterns = [
    path('classrooms', classrooms, name='classrooms'),
    path(
        'classroom/<int:classroom_id>/<str:action>/',
        classrooms_actions,
        name='classroom_actions'
    ),
]

groups_urlpatterns = [
    path('groups', groups, name='groups'),
    path(
        'groups/<int:group_id>/',
        groups_actions,
        name='groups_actions'
    ),
    path('group/<int:group_id>/delete', group_delete, name='group_delete'),
    path(
        'group/<int:group_id>/unpin_student',
        group_unpin_student,
        name='group_unpin_student'
    ),
]

students_urlpatterns = [
    path('students', students, name='students'),
    path(
        'students/<int:student_id>',
        students_actions,
        name='students_actions'
    ),
    path(
        'students/<int:student_id>/<str:action>/',
        students_actions,
        name='students_actions'
    ),
]

teachers_urlpatterns = [
    path('teachers', teachers, name='teachers'),
    path(
        'teacher/<int:teacher_id>/',
        teachers_view,
        name='teachers_actions'
    ),
    path(
        'teacher/<int:teacher_id>/set_lessons_style',
        set_teacher_lessons_style, name='set_teacher_lessons_style',
    ),
    path(
        'teacher/<int:teacher_id>/delete',
        teacher_delete, name='teacher_delete',
    ),
    path(
        'teacher/<int:teacher_id>/unpin_subject',
        unpin_subject, name='unpin_teacher_subject',
    ),
]

invoices_urlpatterns = [
    path('invoices', invoices, name='invoices'),
    path(
        'invoices/<str:action>/<int:invoice_id>/',
        invoices_actions,
        name='invoices_actions'
    ),
    path('invoice/add', invoices_add, name='invoices_add'),
    path(
        'invoice/<int:invoice_id>/change_status',
         invoices_change_status,
         name='invoices_change_status',
    ),
]

services_urlpatterns = [
    path(
        'services/get_service_subjects',
        get_service_subjects,
        name='get_service_subjects'
    ),
    path('services', services, name='services'),
    path(
        'services/<int:service_id>/<str:action>/',
        services_actions,
        name='services_actions'
    ),
]

sources_urlpatterns = [
    path('sources', sources, name='sources'),
    path('sources/<int:source_id>', source_actions,
         name='source_actions'),
    path('sources/<int:source_id>/<str:action>', source_actions_view,
         name='source_actions_view'),

]

presence_urlpatterns = [
    path('presence', presence, name='presence'),
    path(
        'presence/<int:lessons_id>/<str:action>',
        present_actions,
        name='presence_actions'
    ),
]

subject_urlpatterns = [
    path('subject', subject, name='subject'),
    path(
        'subject/<int:subject_id>', subject_view, name='subject_view'
    ),
    path(
        'subject/<int:subject_id>/delete', subject_delete, name='subject_delete'
    ),
]

urlpatterns = [
    path('', home_view, name='home'),
    path('about', home_view, name='about'),
    path('contacts', home_view, name='contacts'),
    path('logout', home_view, name='logout'),
    path('reports', reports, name='reports'),
    path('finance', finance, name='finance')
]

urlpatterns.extend(lessons_urlpatterns)
urlpatterns.extend(event_urlpatterns)
urlpatterns.extend(classrooms_urlpatterns)
urlpatterns.extend(groups_urlpatterns)
urlpatterns.extend(students_urlpatterns)
urlpatterns.extend(teachers_urlpatterns)
urlpatterns.extend(invoices_urlpatterns)
urlpatterns.extend(services_urlpatterns)
urlpatterns.extend(sources_urlpatterns)
urlpatterns.extend(presence_urlpatterns)
urlpatterns.extend(subject_urlpatterns)
