# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

"""
Sayuri's Video Organizer - Base classes

This part is for base classes for inheritance.

""" # (src) core/_base.py

from .. import Config

from pathlib import Path
from argparse import Namespace

from typing import (
    ClassVar,
    Self,
)


# ==================================== Exceptions ==================================== #
class TaskExistsError(RuntimeError): ...  # noqa: E701


# ==================================== Processor ==================================== #
class _Processor:

    _tasks: ClassVar[dict[str, Self]] = {}

    def __new__(cls, config: Config):
        if cls.__name__.startswith('_'):
            raise RuntimeError(
                f"{cls.__name__}: Cannot instantiate abstract or internal class."
            )

        key = str(config.path)

        if key not in cls._tasks:
            cls._tasks[key] = super().__new__(cls)

        else:
            raise TaskExistsError(
                f"{cls.__name__}: Task already exists for {key}."
            )

        return cls._tasks[key]

    def __init__(self, config: Config):
        if not hasattr(self, 'created'):
            self._config = config
            self._path = config.path
            self._args = config.args
            self._debug = config.debug
            self._quiet = config.quiet
            self._quiet_flow = config.quiet_flow
            self._includes = config.includes
            self._excludes = config.excludes
            self._extensions = config.extensions

            self.created = True

    @classmethod
    def get_task(cls, key: str) -> Self:
        return cls._tasks[key]

    @classmethod
    def get_tasks(cls) -> dict[str, Self]:
        return cls._tasks

    @property
    def tasks(self) -> dict[str, Self]:
        return self.get_tasks()

    @property
    def config(self) -> Config:
        return self._config

    @property
    def path(self) -> Path:
        return self._path

    @property
    def args(self) -> Namespace:
        return self._args

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def quiet(self) -> bool:
        return self._quiet

    @property
    def quiet_flow(self) -> bool:
        return self._quiet_flow

    @property
    def includes(self) -> tuple[str, ...]:
        return self._includes

    @property
    def excludes(self) -> tuple[str, ...]:
        return self._excludes

    @property
    def extensions(self) -> tuple[str, ...]:
        return self._extensions


class Processor(_Processor):
    pass
