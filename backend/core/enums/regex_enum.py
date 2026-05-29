from enum import Enum


class RegexEnum(Enum):
    PHONE_NUMBER = (
        r'^(\+380\d{9}|0\d{9})$',
        'Phone number must be in format +380XXXXXXXXX'
    )

    def __init__(self, pattern: str, msg: str):
        self.pattern = pattern
        self.msg = msg

