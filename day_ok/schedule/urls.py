from django.urls import path
from .views import (
    home_view, lessons_view, events_view,
    add_lessons, add_class_room, add_event,
    reports, lessons_actions, event_actions,
    present_actions,
)


urlpatterns = [
    path('', home_view, name='home'),
    path('lessons/add/', add_lessons, name='add_lessons'),
    path('lessons/show_by/<str:show_type>/', lessons_view, name='lessons'),
    path('events', events_view, name='events'),
    path(
        'lessons/present/<str:action>/<int:lessons_id>/',
        present_actions,
        name='present_actions'
    ),
    path('add_class_room', add_class_room, name='add_class_room'),
    path('event/add/', add_event, name='add_event'),
    path('reports', reports, name='reports'),
    path(
        'lessons/<str:action>/<int:lessons_id>/',
        lessons_actions,
        name='lessons_action',
    ),
    path(
        'event/<str:action>/<int:event_id>/',
        event_actions,
        name='events_action',
    ),
]
