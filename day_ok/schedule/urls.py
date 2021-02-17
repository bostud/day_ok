from django.urls import path
from .views import home_view, lessons_view, set_presence, all_present


urlpatterns = [
    path('', home_view, name='home'),
    path('lessons', lessons_view, name='lessons'),
    path('set_presence/<int:lessons_id>/', set_presence, name='set_presence'),
    path('all_present/<int:lessons_id>/', all_present, name='all_present'),
]
