from typing import Optional, List
from ..models import Service, Subject


class Error(Exception):
    pass


class NameAlreadyExistError(Error):
    def __init__(self, name):
        super().__init__(
            f'Ім`я послуги уже існує: {name}.'
        )


def get_service_subjects(service_id: int) -> List[Optional[Subject]]:
    service = Service.objects.filter(id=service_id).first()
    if service:
        return service.subjects.all()
    return []


def get_service(id_: int) -> Optional[Service]:
    return Service.objects.filter(id=id_).first()


def get_all_services() -> List[Optional[Service]]:
    return Service.objects.all()


def add_service(
    name: str,
    price: int,
    lessons_count: int,
    type_of: int,
    subjects: List[int],
) -> Optional[Service]:
    if Service.objects.filter(name=name).first():
        raise NameAlreadyExistError(name)

    subjects = Subject.objects.filter(
        id__in=[int(s_i) for s_i in subjects]
    ).all()
    s = Service(
        name=name,
        price=int(price),
        lessons_count=int(lessons_count),
        type_of=int(type_of),
        subjects=subjects,
    )
    s.save()

    return s


def edit_service(
    service: int,
    name: str,
    price: int,
    lessons_count: int,
    type_of: int,
    subjects: List[int],
) -> Optional[Service]:
    s = Service.objects.filter(id=service).first()
    if s:
        services = Service.objects.filter(name=name).exclude(id=service).all()
        if len(services) > 0:
            raise NameAlreadyExistError(name)
        subjects = [x for x in Subject.objects.filter(
            id__in=[int(s_i) for s_i in subjects]
        ).all()]
        s.name = name
        s.price = price
        s.type_of = type_of
        s.lessons_count = lessons_count
        s.subjects.add(*subjects)
        s.save()

    return s


def delete_subject_from_service(
    service: int,
    subject: int,
) -> Optional[Service]:
    s = Service.objects.filter(id=service).first()
    subject = Subject.objects.filter(id=subject).first()
    if s and subject:
        s.subjects.remove(subject)
        s.save()

    return s
