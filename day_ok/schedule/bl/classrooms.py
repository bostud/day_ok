from typing import List, Optional
from ..models import ClassRoom, Lessons


class Error(Exception):
    pass


class NameAlreadyExistError(Error):
    def __init__(self, name):
        super().__init__(
            f'Ім`я аудиторії уже існує: {name}.'
        )


def get_all_classrooms() -> List[Optional[ClassRoom]]:
    return ClassRoom.objects.all()


def get_classroom_by_id(
    classroom_id: int,
) -> Optional[ClassRoom]:
    return ClassRoom.objects.filter(id=classroom_id).first()


def add_classroom(
    name: str,
    room_type: int,
    places_count: Optional[int] = None,
    description: Optional[str] = None,
) -> Optional[ClassRoom]:
    if ClassRoom.objects.filter(name=name).first():
        raise NameAlreadyExistError(name)

    cl = ClassRoom(
        name=name,
        places_count=places_count or 0,
        room_type=int(room_type),
        description=description or '',
    )
    cl.save()
    return cl


def delete_classroom(
    classroom: int,
    **kwargs,
) -> None:
    pass


def edit_classroom(
    classroom: int,
    name: str,
    room_type: int,
    places_count: Optional[int] = None,
    description: Optional[str] = None,
) -> Optional[ClassRoom]:
    cl = ClassRoom.objects.filter(id=classroom).first()
    if cl:
        cls = ClassRoom.objects.filter(name=name).exclude(id=classroom).all()
        if len(cls) > 0:
            raise NameAlreadyExistError(name)
        cl.name = name
        cl.places_count = places_count
        cl.description = description
        cl.room_type = room_type
        cl.save()

    return cl
