from .base import reports, home_view, about, contacts
from .lessons import lessons_view, add_lessons, lessons_actions
from .events import events, event_actions, event_location
from .teachers import teachers_view, teachers, set_teacher_lessons_style, teacher_delete  # noqa
from .teachers import unpin_subject
from .classrooms import classrooms_actions, classrooms
from .groups import groups, groups_actions, group_delete, group_unpin_student
from .students import students_actions, students
from .invoices import invoices_actions, invoices_add, invoices_change_status
from .invoices import invoices
from .finance import finance
from .services import get_service_subjects, services, services_actions
from .sources import sources, source_actions, source_actions_view
from .present import present_actions, presence
from .subjects import subject, subject_delete, subject_view
