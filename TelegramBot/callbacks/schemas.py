import json
import re
from copy import deepcopy

from typing import Union

from telegram.utils.helpers import escape_markdown

from interfaces.callback_items import ISchema


class BaseSchema(ISchema):
    def __init__(self, path):
        with open(f"schemas/{path}.json", "r") as schema_file:
            self._origin_schema = json.load(schema_file)
        self._keyboard = self._origin_schema.get("keyboard")
        self._message = self._origin_schema.get("message")

    def load_data(self, data: object):
        self._schema = deepcopy(self._origin_schema)
        self._format(self._schema, data)
        self._keyboard = self._schema.get("keyboard")
        self._message = self._schema.get("message")

    def _get_value(self, value: str, data: object):
        dot_loc = value.find(".")
        if dot_loc != -1:
            if isinstance(data, dict):
                new_data = data.get(value[:dot_loc])
            elif isinstance(data, list):
                new_data = data[int(value[:dot_loc])]
            else:
                new_data = getattr(data, value[:dot_loc])
            return self._get_value(value=value[dot_loc + 1 :], data=new_data)
        elif isinstance(data, dict):
            return data.get(value)
        elif isinstance(data, list):
            return data[int(value)]
        else:
            return getattr(data, value)

    def _format(self, iter_: Union[list, dict], data: object):
        if isinstance(iter_, dict):
            iterator = zip(iter_.keys(), iter_.values())
        else:
            iterator = enumerate(iter_)
        for key, value in iterator:
            if isinstance(value, (list, dict)):
                self._format(value, data)
            elif isinstance(value, str):
                if value.startswith("{{ ") and value.endswith(" }}"):
                    formatted_value = self._get_value(
                        value[3:-3].replace("data.", "", 1), data=data
                    )
                    if isinstance(formatted_value, str):
                        formatted_value = escape_markdown(formatted_value, version=2)
                    iter_[key] = formatted_value
                else:
                    to_format = re.findall(r"{{.+}}", iter_[key])
                    for item in to_format:
                        iter_[key] = iter_[key].replace(
                            item,
                            escape_markdown(
                                str(
                                    self._get_value(
                                        item.replace("{{ ", "")
                                        .replace(" }}", "")
                                        .replace("data.", "", 1),
                                        data=data,
                                    )
                                ),
                                version=2,
                            ),
                        )

    @property
    def message(self) -> dict:
        return self._message

    @property
    def keyboard(self) -> dict:
        return self._keyboard


class PageSchema(BaseSchema):
    def __init__(self, path, key):
        super().__init__(path)
        self._origin_message = self._message
        self.key = key

    def load_data(self, data: dict):
        data = data.get(self.key)
        messages = [deepcopy(self._origin_message) for _ in range(len(data.body))]
        for data_instance, message_instance in zip(data.body, messages):
            self._format(message_instance, data_instance)

        print(messages)
        self._message = messages
        self._keyboard.update({"page": data})
