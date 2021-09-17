import re
import datetime


class Field:
    def __init__(self, max_value=None, min_value=1, required=False):
        self.max_value = max_value
        self.min_value = min_value
        self.required = required

    def __get__(self, obj, owner):
        return self.value

    def __set__(self, obj, value):
        if value or self.required:
            self.validate(value)
        self.value = value

    def validate(self, value):
        if self.required and isinstance(value, type(None)):
            raise ValueError("This field is required")


class NumberField(Field):

    def validate(self, value):
        super().validate(value)
        if self.max_value:
            if value > self.max_value:
                raise ValueError("Value is too big!")
        if value < self.min_value:
            raise ValueError("Vale is too small!")


class IntegerField(NumberField):

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, int):
            raise ValueError(f"Value is of not correct type! Should be int, got {type(value)}")
        super().validate(value)


class DecimalField(NumberField):

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, float):
            raise ValueError(f"Value is of not correct type! Should be float, got {type(value)}")
        super().validate(value)


class StringField(Field):

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, str):
            raise ValueError(f"Value is of not correct type! Should be str, got {type(value)}")
        if len(value) > self.max_value:
            raise ValueError("Value is too big!")
        if len(value) < self.min_value:
            raise ValueError("Vale is too small!")


class EmailField(StringField):
    EMAIL_PATTERN = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$")

    def validate(self, value):
        super().validate(value)
        if not re.match(EmailField.EMAIL_PATTERN, value):
            raise ValueError("Phone number is incorrect!")


class DateField(Field):

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, datetime.date):
            raise ValueError(f"Not correct value! Should be date, got {type(value)}")


class PhoneNumberField(StringField):
    PHONE_NUMBER_PATTERN = re.compile("[+]\d{12}")

    def validate(self, value):
        super().validate(value)
        if not re.match(PhoneNumberField.PHONE_NUMBER_PATTERN, value):
            raise ValueError("Phone number is incorrect!")

