from enum import auto

from .auto_name import AutoName


class ButtonStyle(AutoName):
    """Button style type enumeration used in :obj:`~pyrogram.types.KeyboardButton` and :obj:`~pyrogram.types.InlineKeyboardButton`."""

    DEFAULT = auto()
    PRIMARY = auto()
    DANGER = auto()
    SUCCESS = auto()