# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

"""
Sayuri's Video Organizer

This is a tool designed to organize your video files which are ripped from discs or
somewhere else.

It's not supposed to be used for piracy, please don't do that.
But also this tool is under the MIT license, you can use it for your own purpose.

Any questions, please contact me at `catch@463.fish` or `t.me/WhiteFish_Shiromi`.
But I'm not always available, just let you know.

Enjoy~

""" # (src) __init__.py

from .info import _version
__version__ = _version

__all__ = [
    "info",
    "notice",
    "Config",
]

from . import info
from . import notifications as notice
from .config import Config
