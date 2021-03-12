from django.urls import path
from .views import (
    home_view,
    reports,
    lessons_view, lessons_actions, add_lessons,
    events_view, event_actions,
    classrooms, classrooms_actions,
    present_actions,
    groups, groups_actions,
    students_actions, students,
    teachers, teachers_actions,
    invoices, invoices_actions,
    invoices_add, invoices_change_status,
    finance,
)

lessons_urlpatterns = [
    path('lessons/add/', add_lessons, name='add_lessons'),
    path('lessons/show_by/<str:show_type>/', lessons_view, name='lessons'),
    path(
        'lessons/<str:action>/<int:lessons_id>/',
        lessons_actions,
        name='lessons_action',
    ),
    path(
        'lessons/present/<str:action>/<int:lessons_id>/',
        present_actions,
        name='present_actions'
    ),
]

event_urlpatterns = [
    path('events', events_view, name='events'),
    path(
        'event/<str:action>/<int:event_id>/',
        event_actions,
        name='events_action',
    ),
]

classrooms_urlpatterns = [
    path('classrooms', classrooms, name='classrooms'),
    path(
        'classroom/<str:action>/<int:classroom_id>/',
        classrooms_actions,
        name='classroom_actions'
    ),
]

groups_urlpatterns = [
    path('groups', groups, name='groups'),
    path(
        'groups/<str:action>/<int:group_id>/',
        groups_actions,
        name='groups_actions'
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
        'teachers/<str:action>/<int:teacher_id>/',
        teachers_actions,
        name='teachers_actions'
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
