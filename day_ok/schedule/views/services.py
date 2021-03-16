from django.http import HttpRequest, JsonResponse
from ..bl.services import (
    get_service_subjects as service_subjects,
    get_service,
)
from ..forms.services import GetServiceSubjectsForm


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
