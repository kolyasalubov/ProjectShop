from abc import ABC, abstractmethod


class IPage(ABC):
    @property
    @abstractmethod
    def body(self):
        pass

    @property
    @abstractmethod
    def next(self):
        pass

    @property
    @abstractmethod
    def previous(self):
        pass
