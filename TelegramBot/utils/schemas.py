import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import List, Optional, Iterable

from utils.Page import IPage
from utils.image import IImage


@dataclass
class SchematicKeyboard:
    body: list = None
    header: list = None
    footer: list = None
    columns: int = None
    page: IPage = None
    name: str = None
    request_location: str = None
    request_contact: str = None

    def load(self):
        return self.__dict__


class SchematicMessage:
    def __init__(self, text: str = None, image: IImage = None, album: List[IImage] = None, keyboard: dict = None):
        self.text = text
        self.image = image
        self.album = album
        self.keyboard = SchematicKeyboard(**keyboard)


class ISchema(ABC):
    @property
    @abstractmethod
    def message(self) -> SchematicMessage:
        pass


class BaseSchema(ISchema):
    def __init__(self, path, data: object=None):
        with open(path, 'r') as schema_file:
            message = json.load(schema_file)
        if data:
            self._format(message, data)

        self._message = message

    def _get_value(self, value: str, data: object):
        dot_loc = value.find('.')
        if dot_loc != -1:
            new_data = getattr(data, value[:dot_loc])
            self._get_value(value=value[dot_loc+1:], data=new_data)
        else:
            return getattr(data, value)

    def _format(self, iter_: Optional[list, dict], data: object):
        if isinstance(iter_, dict):
            iterator = zip(iter_.keys(), iter_.values())
        else:
            iterator = enumerate(iter_)
        for key, value in iterator:
            if isinstance(value, Iterable):
                self._format(value, data)
            else:
                if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                    self._get_value(value.replace("{", "").replace("}", "").replace("data.", ""), data=data)

    @property
    def message(self) -> SchematicMessage:
        return SchematicMessage(**self._message)
