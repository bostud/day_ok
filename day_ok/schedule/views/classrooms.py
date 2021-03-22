from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from ..middleware import authenticated
from ..bl.classrooms import (
    get_all_classrooms, add_classroom,
    delete_classroom, get_classroom_by_id,
    edit_classroom,
)
from ..forms.classrooms import (
    AddClassRoomForm, DeleteClassRoomForm, EditClassRoomForm
)
from ..forms.utils import METHOD_DELETE, METHOD_EDIT


@authenticated
def classrooms(request: HttpRequest):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/classroom/base.html'

    def _view_all():
        ctx.update(classrooms=get_all_classrooms())
        ctx.update(form=AddClassRoomForm())

    def _create():
        form = AddClassRoomForm(request.POST)
        if form.is_valid():
            add_classroom(**form.cleaned_data)

    if request.method == 'POST':
        _create()

    _view_all()

    return render(request, template_name, ctx)


@authenticated
def classrooms_actions(request: HttpRequest, classroom_id: int, action: str):
    ctx: Dict[Any, Any] = {}
    template_name = 'schedule/sources/view.html'

    if request.method == 'POST':
        if action == METHOD_DELETE:
            form = DeleteClassRoomForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['method'] == METHOD_DELETE:
                    delete_classroom(classroom_id)
        elif action == METHOD_EDIT:
            form = EditClassRoomForm(request.POST)
            if form.is_valid():
                edit_classroom(**form.cleaned_data)
    else:
        classroom = get_classroom_by_id(classroom_id)
        ctx['delete_form'] = DeleteClassRoomForm({
            'classroom': classroom_id,
            'method': METHOD_DELETE,
        })
        ctx['edit_form'] = EditClassRoomForm()
        ctx['classroom'] = classroom
        return render(request, template_name, ctx)
    return HttpResponseRedirect('/schedule/classrooms')
