from ..models import Group


def groups_objects():
    return Group.objects.all()
