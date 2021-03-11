from dataclasses import dataclass


@dataclass
class SourceDataClass:
    name: str
    count: int
    percent: float
    percent_view: float = 0

