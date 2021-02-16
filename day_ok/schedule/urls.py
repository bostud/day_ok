from django.urls import path, re_path
from .views import home_view, lessons_view


urlpatterns = [
    path('', home_view, name='home'),
    re_path(r'^lessons/?', lessons_view, name='lessons'),
]
