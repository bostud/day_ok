from typing import Dict, Any
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from ..bl.services import (
    get_service_subjects as service_subjects,
    get_service, get_all_services,
    add_service,
    edit_service,
    delete_subject_from_service,
    NameAlreadyExistError,
)
from ..middleware import authenticated
from ..forms.services import (
    GetServiceSubjectsForm,
    ServiceForm,
    DeleteSubjectFromServiceForm,
)
from ..forms.validators import METHOD_DELETE, METHOD_EDIT


@authenticated
def get_service_subjects(request: HttpRequest):
    if request.method == 'GET':
        form = GetServiceSubjectsForm(request.GET)
        if form.is_valid():
            service_id = int(form.cleaned_data['service'])
            service = get_service(service_id)
            result = [(r.id, r.name) for r in service_subjects(service_id)]
            return JsonResponse(
                {
                    'status': 'OK',
                    'result': result,
                    'service': {
                        'type_of_title': service.type_of_title,
                        'price': service.price,
                        'lessons_count': service.lessons_count,
                    }
                },
                status=200,
            )
    return JsonResponse({}, status=400)


@authenticated
def services(request: HttpRequest):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/services/base.html'

    def _view_all(add_form: bool = False):
        ctx.update(services=get_all_services())
        if add_form:
            ctx.update(form=ServiceForm())

    def _create():
        form = ServiceForm(request.POST)
        if form.is_valid():
            try:
                add_service(**form.cleaned_data)
            except Exception as e:
                ctx.update(errors=e)
                ctx.update(form=ServiceForm(data=form.cleaned_data))

    if request.method == 'POST':
        _create()

    _view_all()

    return render(request, template_name, ctx)


@authenticated
def services_actions(request: HttpRequest, service_id: int, action: str):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/services/view.html'

    if request.method == 'POST':
        if action == METHOD_DELETE:
            form = DeleteSubjectFromServiceForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('/schedule/classrooms')
        elif action == METHOD_EDIT:
            form = ServiceForm(request.POST)
            if form.is_valid():
                try:
                    edit_service(service_id, **form.cleaned_data)
                    ctx.update(status='success')
                except NameAlreadyExistError as e:
                    ctx.update(errors=e)
        elif action == 'delete_subject':
            form = DeleteSubjectFromServiceForm(request.POST)
            if form.is_valid():
                delete_subject_from_service(
                    service_id, form.cleaned_data['subject'])

    service = get_service(service_id)
    data = model_to_dict(service)
    ctx['edit_form'] = ServiceForm(data=data)
    ctx['service'] = service
    return render(request, template_name, ctx)
