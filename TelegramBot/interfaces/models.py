from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class IPage(ABC):
    body: list
    next: str
    previous: str


class IPaginatedModel(ABC):
    @classmethod
    @abstractmethod
    def get(cls, *args, **kwargs) -> IPage:
        pass

    @classmethod
    @abstractmethod
    def turn_page(cls, url: str) -> IPage:
        pass


class IImage(ABC):
    @abstractmethod
    def get(self) -> bytes:
        pass
