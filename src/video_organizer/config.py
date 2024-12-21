# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

"""
Sayuri's Video Organizer - Configuration

Every process request requires a configuration instance.
Use `Config` class to create a configuration instance.

For more information, see documentation or `Config` class.

""" # (src) config.py

from . import info

from argparse import (
    Namespace,
    ArgumentParser,
)

from pathlib import Path

from collections.abc import Sequence
from typing import (
    ClassVar,
    Self,
)

# ===================================== Constants ==================================== #
SUPPORTED_EXTENSIONS: tuple[str, ...] = (
    '.mkv',
    '.mp4',
    '.avi',
    '.mov',
    '.wmv',
)


# =================================== Configuration ================================== #
class _Config:
    """
    Internal configuration class that handles parsing and storing configuration options.

    *You're not supposed to use this class directly.
    """

    _default: ClassVar[Self]

    _created: bool

    _parser: ArgumentParser
    _args: Namespace

    _debug: bool
    _quiet: bool
    _quiet_flow: bool
    _info: bool
    _path: Path
    _output: Path
    _save: bool
    _no_subdir: bool
    _includes: tuple[str, ...]
    _excludes: tuple[str, ...]
    _extensions: tuple[str, ...]

    def __new__(cls, internal_args: Sequence[str] | None, *args, **kwargs) -> Self:
        if cls.__name__.startswith('_'):
            raise RuntimeError(
                f"{cls.__name__}: Cannot instantiate abstract or internal class."
            )

        if not hasattr(cls, '_default'):
            cls._default = super().__new__(cls)

        return cls._default

    # ----------------------------- Initialize Options ------------------------------- #
    def __init__(self, internal_args: Sequence[str] | None) -> None:
        if not hasattr(self, '_created'):
            parser = self._add_arguments(
                ArgumentParser(
                    prog=info._project,
                    description=info._description,
                )
            )
            self._parser = parser
            self._args = parser.parse_args(internal_args)

            self._debug = self._args.debug
            self._quiet = self._args.quiet
            self._quiet_flow = self._args.quiet_flow

            self._info = self._args.info

            self._path = Path(self._args.path)
            self._output = Path(self._args.output)
            self._save = self._args.save
            self._no_subdir = self._args.no_subdir
            self._includes = self._strip_args(self._args.includes)
            self._excludes = self._strip_args(self._args.excludes)
            self._extensions = (
                self._strip_args(self._args.extensions) or SUPPORTED_EXTENSIONS
            )

            self._created = True

    # ------------------------------- Class Methods ---------------------------------- #
    @classmethod
    def get_config(cls) -> Self:
        """Get the existing configuration"""
        return cls._default

    # ------------------------------ Private Methods --------------------------------- #
    def _strip_args(self, arg: str) -> tuple[str, ...]:
        """Strip a string argument to return a tuple of strings"""
        return tuple(x.strip() for x in arg.split(',') if x.strip())

    def _add_arguments(self, parser: ArgumentParser) -> ArgumentParser:
        """Add arguments to the parser"""
        # -------------------------- Basic Arguments --------------------------------- #
        parser.add_argument(
            '-V',
            '--version',
            action='version',
            version=f"%(prog)s {info._version}",
        )

        parser.add_argument(
            '--debug',
            action='store_true',
            help="Enable debug mode.",
        )

        parser.add_argument(
            '-Q',
            '--quiet',
            action='store_true',
            help="Display necessary messages only.",
        )

        parser.add_argument(
            '-qf',
            '--quiet-flow',
            action='store_true',
            help="Display less messages.",
        )

        # ------------------------- Process Arguments -------------------------------- #
        parser.add_argument(
            '-I',
            '--info',
            action='store_true',
            help="Display the information only.",
        )

        # ------------------------ Additional Arguments ------------------------------ #
        parser.add_argument(
            '-P',
            '--path',
            default='.',
            help=(
                "The path to the directory/file to process. "
                "(default: current directory)"
            ),
        )

        parser.add_argument(
            '-O',
            '--output',
            default='.',
            help="The path to the output directory. (default: current directory)",
        )

        parser.add_argument(
            '-S',
            '--save',
            action='store_true',
            help="Edit the files directly without backup.",
        )

        parser.add_argument(
            '--no-subdir',
            action='store_true',
            help="Do not process the subdirectories.",
        )

        parser.add_argument(
            '-inc',
            '--includes',
            default='',
            help=(
                "Only process the directories/files which contain the keywords. "
                "Split by ',' to include multiple keywords."
            ),
        )

        parser.add_argument(
            '-exc',
            '--excludes',
            default='',
            help=(
                "Exclude the directories/files which contain the keywords. "
                "Split by ',' to exclude multiple keywords."
            ),
        )

        parser.add_argument(
            '-ext',
            '--extensions',
            default='',
            help=(
                "Only process the specific extensions of the files. "
                "Similar to `--include`, but only process the extensions.\n"
                "Split by ',' to include multiple extensions."
            ),
        )

        return parser

    # --------------------------------- Properties ----------------------------------- #
    @property
    def parser(self) -> ArgumentParser:
        """Argument parser"""
        return self._parser

    @property
    def args(self) -> Namespace:
        """Parsed arguments"""
        return self._args

    @property
    def debug(self) -> bool:
        """Debug mode"""
        return self._debug

    @property
    def quiet(self) -> bool:
        """Disable messages unless necessary."""
        return self._quiet

    @property
    def quiet_flow(self) -> bool:
        """Show less messages."""
        return self._quiet_flow

    @property
    def info(self) -> bool:
        """Display the information only."""
        return self._info

    @property
    def no_subdir(self) -> bool:
        """Disable processing subdirectories search."""
        return self._no_subdir

    @property
    def save(self) -> bool:
        """Edit the files directly without backup."""
        return self._save

    @property
    def path(self) -> Path:
        """Target directory or file."""
        return self._path

    @property
    def output(self) -> Path:
        """Output directory"""
        return self._output

    @property
    def includes(self) -> tuple[str, ...]:
        """Keywords to include for search."""
        return self._includes

    @property
    def excludes(self) -> tuple[str, ...]:
        """Keywords to exclude for search."""
        return self._excludes

    @property
    def extensions(self) -> tuple[str, ...]:
        """Specific extensions to process"""
        return self._extensions


class Config(_Config):
    """
    Public Configuration class that extends the `_Config` base class.
    There should be only one instance created of this class.

    To get existing configuration, use `get_config()` method.

    Properties:
        - `debug` (bool): Enable debug mode.
        - `quiet` (bool): Disable messages unless necessary.
        - `quiet_flow` (bool): Disable flow messages.
        - `info` (bool): Only display the information without editing the files.
        - `path` (Path): Path to the target directory or file.
        - `output` (Path): Path to the output directory.
        - `save` (bool): Flag to save changes without backup.
        - `no_subdir` (bool): Disable processing subdirectories search.
        - `includes` (tuple[str, ...]): Keywords to include for search.
        - `excludes` (tuple[str, ...]): Keywords to exclude for search.
        - `extensions` (tuple[str, ...]): Only process following extensions.

        - `args` (Namespace): Parsed arguments.
    """
    __slots__ = (
        '_created',
        '_parser',
        '_args',
        '_debug',
        '_quiet',
        '_quiet_flow',
        '_info',
        '_path',
        '_output',
        '_save',
        '_no_subdir',
        '_includes',
        '_excludes',
        '_extensions',
    )
