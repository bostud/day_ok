from typing import Optional
from ..models import Group


def groups_objects():
    return Group.objects.all()


def get_group(id_: int) -> Optional[Group]:
    return Group.objects.filter(id=id_).first()
