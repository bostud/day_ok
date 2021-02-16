from typing import Optional, List
from django.shortcuts import loader, render
from django.http import HttpResponse, HttpRequest
# Create your views here.
from .middleware import authenticated
from datetime import datetime, timedelta

from .forms import LessonsForm
from .models import ClassRoom
from .controllers.lessons import get_weekly_class_room_lessons_by_day
from .utils import get_weekday_number, get_weekday_name


@authenticated
def home_view(request: HttpRequest, *args, **kwargs):
    template = loader.get_template('schedule/base/base_cms.html')
    return HttpResponse(template.render(request=request))


@authenticated
def lessons_view(request: HttpRequest, *args, **kwargs):
    context = {
        'form': LessonsForm(),
        'weekly_schedule': None,
    }
    if request.method == 'POST':
        form = LessonsForm(request.POST)
        if form.is_valid():
            class_room = int(form['class_room'].value())
            date_from = datetime.strptime(
                form['date_from'].value(),
                '%m/%d/%Y'
            ).date()
            weekly_schedule = get_weekly_class_room_lessons_by_day(
                class_room,
                date_from
            )
            context['lessons_date_from'] = date_from.strftime('%d.%m.%Y')
            context['lessons_date_to'] = (
                    date_from + timedelta(days=7)
            ).strftime('%d.%m.%Y')
            context['selected_class_room'] = (
                ClassRoom.objects.get(id=class_room).name
            )
            week_days_names = ([
                get_weekday_name(get_weekday_number(
                    datetime.strptime(dt, '%d.%m.%Y')))
                for dt in weekly_schedule
            ])
            context['total_schedule'] = list(zip(
                week_days_names,
                weekly_schedule.values(),
                weekly_schedule.keys(),
            ))
            print(context['total_schedule'])

    return render(request, 'schedule/lessons.html', context)
