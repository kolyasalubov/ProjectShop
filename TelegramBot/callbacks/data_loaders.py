from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from telegram import Update
from telegram.ext import CallbackContext
from typing import Iterable

from client.models import User
from interfaces.callback_items import IContextLoader, IPaginatedModelLoader, IDataLoader
from interfaces.models import IPaginatedModel


@dataclass
class ChatDataLoader(IContextLoader):
    key: Iterable[str] | str
    alias: Iterable[str] | str = tuple()

    def _normalize_attributes(self):
        if isinstance(self.key, str):
            self.key = (self.key,)
        if isinstance(self.alias, str):
            self.alias = (self.alias,)

    def _resolve_key(self, key):
        try:
            return self.alias[self.key.index(key)]
        except IndexError:
            return key

    def load(self, update: Update, context: CallbackContext) -> dict:
        self._normalize_attributes()
        return {
            self._resolve_key(key): context.chat_data.get("memory").get(key)
            for key in self.key
        }


@dataclass
class UpdateTextLoader(IContextLoader):
    name: str

    def load(self, update: Update, context: CallbackContext) -> dict:
        return {self.name: update.message.text}


@dataclass
class CallbackDataLoader(IContextLoader):
    alias: str = None

    def load(self, update: Update, context: CallbackContext) -> dict:
        key, value = update.callback_query.data.split("=", 1)
        if self.alias:
            return {self.alias: value}
        else:
            return {key: value}


class TelegramIdLoader(IContextLoader):
    def load(self, update: Update, context: CallbackContext) -> dict:
        return {"telegram_id": update.message.from_user.id}


@dataclass
class BasePageModelLoader(IPaginatedModelLoader):
    model: type(IPaginatedModel)
    data: IContextLoader = None

    @property
    @abstractmethod
    def method(self) -> str:
        pass

    @method.setter
    @abstractmethod
    def method(self, method: str):
        pass

    def load(self, update: Update = None, context: CallbackContext = None) -> dict:
        if self.data:
            data = self.data.load(update, context)
        else:
            data = {}
        return {self.model.__name__.lower(): getattr(self.model, self.method)(**data)}


class FirstPageModelLoader(BasePageModelLoader):
    method = "get"


class TurnPageModelLoader(BasePageModelLoader):
    method = "turn_page"


@dataclass
class ModelInstanceLoader(IPaginatedModelLoader):
    model: type(IPaginatedModel)
    data: IContextLoader = None

    def load(self, update: Update = None, context: CallbackContext = None) -> dict:
        if self.data:
            data = self.data.load(update, context)
        else:
            data = {}
        instance = self.model.get_one(**data)
        return {self.model.__name__.lower(): instance}


@dataclass
class BaseUserLoader(IDataLoader):
    data: IContextLoader | Iterable[IContextLoader]
    instance = User

    @property
    @abstractmethod
    def method(self) -> str:
        pass

    @method.setter
    @abstractmethod
    def method(self, method: str):
        pass

    def _normalize_attributes(self):
        if isinstance(self.data, IContextLoader):
            self.data = (self.data,)

    def load(self, update: Update = None, context: CallbackContext = None):
        self._normalize_attributes()
        data = {}
        for loader in self.data:
            data.update(loader.load(update, context))

        if "name" in data:
            data["first_name"], data["last_name"] = data["name"].split()
            del data["name"]

        user = getattr(self.instance, self.method)(**data)
        return {"user": user}


class RegisterUserLoader(BaseUserLoader):
    method = "register_user"


class UpdateUserLoader(BaseUserLoader):
    method = "update"

    def load(self, update: Update = None, context: CallbackContext = None):
        self.instance = ChatDataLoader("user").load(update, context)
        super().load(update, context)
