# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

"""
Sayuri's Video Organizer - Media Info

Get the media information.

""" # (src) core/_media_info.py

from .. import (
    notice,
    Config,
)

from ._base import Processor

from .identify import (
    MediaInfo,
)

from pathlib import Path
from collections import defaultdict

# ==================================== Constants ===================================== #
SUPPORTED_EXTENSIONS: tuple[str, ...] = (
    'mp4',
    'mkv',
    'avi',
    'mov',
    'wmv',
)


# ======================================= Core ======================================= #
class _MediaProcessor(Processor):

    _data: defaultdict[int, MediaInfo]
    _total_files: int

    def __init__(self, config: Config):
        if not hasattr(self, 'created'):
            super().__init__(config)
            _target_files = self._search_files(self.path)
            self._total_files = self._count_files(_target_files)
            self._data = self._get_media_info(_target_files)

    def _count_files(self, files: list[Path]) -> int:
        count = len(files)
        notice.notice_found_files(count)

        if not any([self.quiet, self.quiet_flow, not count]):
            print("Files:")
            for file in files:
                print(file)

        return count

    def _filter(self, file: Path) -> bool:
        if file.is_dir():
            if any([
                self.includes and not any(
                    keyword in file.name for keyword in self.includes
                ),
                self.excludes and any(
                    keyword in file.name for keyword in self.excludes
                ),
            ]):
                return False

        elif file.is_file():
            if any([
                self.includes and not any(
                    keyword in file.name for keyword in self.includes
                ),
                self.excludes and any(
                    keyword in file.name for keyword in self.excludes
                ),
                self.extensions and file.suffix not in self.extensions,
            ]):
                return False

        return True  # file is to be processed

    def _search_files(self, path: Path, target_files: list[Path] = []) -> list[Path]:
        """ Search target files in the directory """
        if not path.exists():
            raise FileNotFoundError(f"The path {path} does not exist.")

        # When the path is a file
        if path.is_file():
            if self.debug:
                print(f"[DEBUG] {path} is a file.")
                print(f"[DEBUG] Target file: {path}")
                print()

            if self._filter(path):
                target_files.append(path)

        # When the path is a directory
        elif path.is_dir():
            # pattern = '*' if no_subdir else '**/*'
            for f in path.iterdir():
                if not self._filter(f):
                    if self.debug:
                        print(f"[DEBUG] Filter to skip: {f}")
                    continue

                if f.is_dir():
                    if self.args.no_subdir:
                        if self.debug:
                            print(f"[DEBUG] `--no-subdir` skipping {f}")
                        continue

                    if self.debug:
                        print(f"[DEBUG] Finding files in {f}")

                    self._search_files(
                        f,
                        target_files,  # reference to the same list don't need extend
                    )

                elif f.is_file():
                    if self.debug:
                        print(f"[DEBUG] Found {f}")
                    target_files.append(f)

        return target_files

    def _get_media_info(self, target_files: list[Path]) -> defaultdict[int, MediaInfo]:
        if not self.debug and not self.quiet:
            notice.notice_search_options(self.includes, self.excludes, self.extensions)
            print("Getting files...\n")

        data = defaultdict[int, MediaInfo](lambda: MediaInfo(Path(), self.debug))

        extracted = 0

        for processing, file in enumerate(target_files, 1):
            print(f'Processing file {processing} of {self.total_files}')
            match file.suffix:
                case '.mkv':
                    extracted += 1
                    data[extracted] = MediaInfo(file, self.debug)
                    print(f'{data[extracted].name=}')
                    print(f'{data[extracted].path=}')
                    # print(f'{data[extracted].get(1).codec=} ')
                    # print(f'{info._video_tracks=} ')
                    # print(f'{info._audio_tracks=} ')
                    # print(f'{info._subtitle_tracks=} ')
                    print(f'{data[extracted].total_tracks=} ')
                    print(f'{data[extracted].total_video_tracks=} ')
                    print(f'{data[extracted].total_audio_tracks=} ')
                    print(f'{data[extracted].total_subtitle_tracks=} ')
                    print(f'{data[extracted].total_fonts=} ')

        return data

    @property
    def total_files(self) -> int:
        return self._total_files

    @property
    def data(self) -> defaultdict[int, MediaInfo]:
        return self._data


class MediaProcessor(_MediaProcessor):
    slots = (
        '_config',
        '_path',
        '_args',
        '_debug',
        '_quiet',
        '_quiet_flow',
        '_includes',
        '_excludes',
        '_extensions',
        '_total_files',
        '_data',
    )
