from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Union

from telegram import Update, Message, ReplyMarkup
from telegram.ext import CallbackContext

from interfaces.models import IPaginatedModel


class ISchema(ABC):
    @property
    @abstractmethod
    def message(self) -> dict:
        pass

    @property
    @abstractmethod
    def keyboard(self) -> dict:
        pass

    @abstractmethod
    def load_data(self, data: object):
        pass


class IDataLoader(ABC):
    @abstractmethod
    def load(self, *args, **kwargs) -> dict:
        pass


class IContextLoader(IDataLoader):
    def load(self, update: Update, context: CallbackContext) -> dict:
        pass


@dataclass
class IPaginatedModelLoader(IDataLoader, ABC):
    model: type(IPaginatedModel)


class IDataSaver(ABC):
    @abstractmethod
    def save(self, context: CallbackContext, name: str, value: object):
        pass


class IMessageHistoryManager(ABC):
    @abstractmethod
    def save(
        self, context: CallbackContext, name, message: Union[Message, List[Message]]
    ):
        pass

    @abstractmethod
    def load(self, context: CallbackContext, name) -> Union[Message, List[Message]]:
        pass

    @abstractmethod
    def delete(self, update: Update, context: CallbackContext, name_field: str):
        pass

    @abstractmethod
    def delete_with_interval(
        self, context: CallbackContext, name_field: str, interval: int
    ):
        pass

    @abstractmethod
    def clean(self, context: CallbackContext, name_field: str):
        pass


class IMessageBuilder(ABC):
    @property
    @abstractmethod
    def reply_markup(self) -> Union[ReplyMarkup, List[ReplyMarkup]]:
        pass

    @abstractmethod
    def send(self, data: dict) -> Union[Message, List[Message]]:
        pass


class IMessageAlter(ABC):
    @property
    @abstractmethod
    def reply_markup(self) -> Union[ReplyMarkup, List[ReplyMarkup]]:
        pass

    @abstractmethod
    def edit(self):
        pass


class IMessageRebuilder(ABC):
    @abstractmethod
    def send(self, data: dict) -> Union[Message, List[Message]]:
        pass


class IMenuBuilder(ABC):
    @property
    @abstractmethod
    def keyboard(self) -> ReplyMarkup:
        pass


class ICallbackClass(ABC):
    @abstractmethod
    def __call__(self, update: Update, context: CallbackContext):
        pass
