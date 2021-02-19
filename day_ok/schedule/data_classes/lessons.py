from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, date


class Base:
    def to_dict(self, key_prefix: str = '') -> dict:
        return {
            self.get_key_name(k, key_prefix): v
            for k, v in self.__dict__
        }

    @staticmethod
    def get_key_name(key, key_prefix = '') -> str:
        return f"{key_prefix}_{key}" if key_prefix else f"{key}"


@dataclass
class AddLessonsDC(Base):
    class_rooms: list
    lessons_types: list
    subjects: list
    teachers: list
    students: list
    groups: list
    weekdays: tuple


@dataclass
class EditLessonsDC(Base):
    class_room: int
    date_from_valid: datetime
    time_start: datetime
    lessons_type: int
    teacher: int
    student: int
    parent: int
    group: int = None
    subject: int = None

    weekdays_for_repeating: Optional[List[int]] = None
    date_until_valid: datetime = None
    time_end: datetime = None
    change_all: bool = False

    def to_dict(self, **kwargs) -> dict:
        return super().to_dict('edit')
