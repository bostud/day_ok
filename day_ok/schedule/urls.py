from django.urls import path
from .views import (
    home_view, lessons_view,
    set_present, all_present, events_view,
    add_lessons, add_class_room, add_event,
    reports, edit_lessons, edit_event,
)


urlpatterns = [
    path('', home_view, name='home'),
    path('lessons/<str:show_type>/', lessons_view, name='lessons'),
    path('events', events_view, name='events'),
    path('set_present/<int:lessons_id>/', set_present, name='set_present'),
    path('all_present/<int:lessons_id>/', all_present, name='all_present'),
    path('add_class_room', add_class_room, name='add_class_room'),
    path('add_lessons', add_lessons, name='add_lessons'),
    path('add_event', add_event, name='add_event'),
    path('reports', reports, name='reports'),
    path('edit_lessons/<int:lessons_id>/', edit_lessons, name='edit_lessons'),
    path('edit_event/<int:lessons_id>/', edit_event, name='edit_event'),
]
