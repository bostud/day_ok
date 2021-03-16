from typing import Optional, List
from ..models import Service, Subject


def get_service_subjects(service_id: int) -> List[Optional[Subject]]:
    service = Service.objects.filter(id=service_id).first()
    if service:
        return service.subjects.all()
    return []


def get_service(id_: int) -> Optional[Service]:
    return Service.objects.filter(id=id_).first()
