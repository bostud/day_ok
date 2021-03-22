from ..models import Source


METHOD_DELETE = 'delete'
METHOD_EDIT = 'edit'
AVAILABLE_METHODS = [
   METHOD_DELETE,
   METHOD_EDIT,
]


def validate_delete_method(value: str) -> bool:
    return value == METHOD_DELETE


def validate_edit_method(value: str) -> bool:
    return value == METHOD_EDIT


def validate_source_name(value: str) -> bool:
    return Source.objects.filter(name=value.strip()).count() == 0
