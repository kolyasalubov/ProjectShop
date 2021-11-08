from abc import ABC, abstractmethod

from typing import List


class IImage(ABC):
    @abstractmethod
    def get(self) -> bytes:
        pass
