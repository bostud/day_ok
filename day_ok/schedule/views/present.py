from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from ..middleware import authenticated
from ..bl.lessons import all_presence


@authenticated
def present_actions(request: HttpRequest, action: str, lessons_id: int):
    ctx = {}
    template_name = 'schedule/lessons/main.html'

    def _all_present():
        all_presence(lessons_id)
        return HttpResponseRedirect(
            '/schedule/' + str(request.headers['Referer'].split('/')[-1])
        )

    def _edit_present():
        pass

    def _clean_present():
        pass

    action_func = {
        'edit': _edit_present,
        'all': _all_present,
        'clean': _clean_present,
    }
    if f := action_func.get(action):
        f()
    else:
        ctx = {
            'errors': [f'Невірна дія: {action}']
        }
    return render(request, template_name, ctx)
