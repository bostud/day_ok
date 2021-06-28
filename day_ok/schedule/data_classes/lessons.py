from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, date
from ..models import Teacher, Lessons


class Base:
    def to_dict(self, key_prefix: str = '') -> dict:
        return {
            self.get_key_name(k, key_prefix): v
            for k, v in self.__dict__.items()
        }

    @staticmethod
    def get_key_name(key, key_prefix = '') -> str:
        return f"{key_prefix}_{key}" if key_prefix else f"{key}"


@dataclass
class AddLessonsDC(Base):
    classrooms: list
    lessons_types: list
    subjects: list
    teachers: list
    students: list
    groups: list
    weekdays: tuple


@dataclass
class EditLessonsDC(Base):
    classroom: int
    date_from_valid: datetime
    time_start: datetime
    lessons_type: int
    teacher: int
    parent: int
    subject: int
    group: int = None
    student: int = None

    weekdays_for_repeating: Optional[List[int]] = None
    date_until_valid: datetime = None
    change_all: bool = False

    def to_dict(self, **kwargs) -> dict:
        return super().to_dict('edit')


@dataclass
class LessonsScheduleTeachers(Base):
    teacher: Teacher
    date: date
    lessons: List[Lessons]


@dataclass
class EmptyLessons(Base):
    time_start: datetime.time
    is_empty: bool = True
    duration: int = 30


@dataclass
class LessonsDayWeekView(Base):
    date_name: str
    date: datetime.date
    is_today: bool
    lessons: List[Lessons]
    head_color: str
