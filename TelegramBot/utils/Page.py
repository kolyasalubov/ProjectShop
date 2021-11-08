from abc import ABC
from dataclasses import dataclass


@dataclass
class IPage(ABC):
    body: list
    next: str
    previous: str
