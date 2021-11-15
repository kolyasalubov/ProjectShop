from __future__ import annotations

from dataclasses import dataclass
from typing import List, Iterable, Union

from telegram import Message, Update
from telegram.ext import CallbackContext

from interfaces.callback_items import IMessageHistoryManager
from callbacks.exceptions import NameFieldError


@dataclass
class MessageHistoryManager(IMessageHistoryManager):
    save_in_history: bool = False

    def save(
        self,
        context: CallbackContext,
        name: str,
        message: Union[Message, List[Message]],
    ):
        if "message" not in context.chat_data:
            context.chat_data["message"] = {}
        elif name in context.chat_data["message"]:
            raise NameFieldError(name)
        context.chat_data["message"][name] = message

    def load(self, context: CallbackContext, name) -> Union[Message, List[Message]]:
        return context.chat_data["message"][name]

    def _delete_iter(self, iter_: Message | Iterable):
        if isinstance(iter_, Iterable):
            for item in iter_:
                self._delete_iter(item)
        else:
            iter_.delete()

    def delete(self, update: Update, context: CallbackContext, name_field: str):
        if name_field == "update":
            message = update.message or update.callback_query.message
            message.delete()
        else:
            print(context.chat_data["message"])
            messages = context.chat_data["message"][name_field]
            self._delete_iter(messages)

            if not self.save_in_history:
                del context.chat_data["message"][name_field]

    def _delete_with_interval(self, context):
        self._delete_iter(context.job.context)

    def delete_with_interval(
        self, context: CallbackContext, name_field: str, interval: int
    ):
        message = context.chat_data["message"][name_field]
        del context.chat_data["message"][name_field]

        context.job_queue.run_once(
            when=interval, callback=self._delete_with_interval, context=message
        )

    def clean(self, context: CallbackContext, name_field: str):
        del context.chat_data["message"][name_field]
