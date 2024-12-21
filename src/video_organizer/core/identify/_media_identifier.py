# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

""" Media Identify
Recognize media files and extract metadata.

Supported:
    - Video
    - Audio
    - Subtitle
    - Font

! Required:
    - ffprobe

""" # (src) core/identify/_media_identifier.py

from dataclasses import (
    dataclass,
    field,
)

from pathlib import Path
import shutil
import subprocess
import json

from . import base

from typing import (
    Any,
    Optional,
    ClassVar,
    Self,
)


type TrackTypes = VideoTrack | AudioTrack | SubtitleTrack | AttachTrack


# ==================================== Exceptions ==================================== #
class QueryError(Exception): ...  # noqa: E701
class CreationError(Exception): ...  # noqa: E701


# =================================== Data Classes =================================== #
@dataclass(slots=True)
class FormatData:
    score: int
    size: int
    duration: float
    duration_str: str
    format: str
    format_long_name: str
    bitrate: int
    encoder: str
    encoding_info: str


@dataclass(slots=True)
class VideoTrack:
    index: Optional[int] = field(
        metadata={
            "description": "The index of the tracks (Not in this category only)."
        }
    )
    default: bool
    forced: bool
    codec: str
    language: str
    duration: str
    duration_sec: float
    fps: float
    bps: int
    display_dimensions: str
    display_width: int
    display_height: int
    display_aspect_ratio: str
    display_resolution: str
    pixel_width: int
    pixel_height: int
    pixel_dimensions: str
    pixel_format: str
    color_range: str
    color_space: str
    color_transfer: str
    color_primaries: str


@dataclass(slots=True)
class AudioTrack:
    index: Optional[int] = field(
        metadata={
            "description": "The index of the tracks (Not in this category only)."
        }
    )
    codec: str
    channels: int
    sample_rate: int
    language: str
    bit_depth: int
    duration: float


@dataclass(slots=True)
class SubtitleTrack:
    index: Optional[int] = field(
        metadata={
            "description": "The index of the tracks (Not in this category only)."
        }
    )
    codec: str
    language: str
    forced: bool
    default: bool
    hearing_impaired: bool
    visual_impaired: bool
    font_name: str
    mimetype: str
    duration: float


@dataclass(slots=True)
class AttachTrack:
    index: Optional[int]
    codec: str
    filename: str
    mimetype: str
    disposition: dict[str, Any]


class _MediaInfo:
    """ Internal class for MediaInfo, please call MediaInfo instead. """

    _debug_mode: ClassVar[bool] = False

    _files: ClassVar[dict[str, Self]] = {}
    _total_file_size: ClassVar[int] = 0

    def __new__(cls, file_path: Path, *args, **kwargs) -> Self:
        if cls.__name__.startswith('_'):
            raise RuntimeError(
                f"{cls.__name__}: Cannot instantiate abstract or internal class."
            )

        if file_path not in cls._files:
            file = super().__new__(cls)
            cls._files[str(file_path)] = file

        return cls._files[str(file_path)]

    def __init__(self, file_path: Path, debug: bool = False):
        if not hasattr(self, 'created'):
            self.debug = debug  # Property setter
            self._file_path = file_path

            self._raw_info: dict[str, Any] = self._get_raw_data()
            self._format_data: FormatData = self._get_format_data()

            self._tracks: dict[int, str] = {}
            self._tracks_by_type: dict[str, list[int]] = {}
            self._video_tracks: dict[int, VideoTrack] = {}
            self._audio_tracks: dict[int, AudioTrack] = {}
            self._subtitle_tracks: dict[int, SubtitleTrack] = {}
            self._attach_tracks: dict[int, AttachTrack] = {}
            self._attach_fonts: int = 0

            self._get_tracks_data()

            self.created = True

    # ------------------------------- Class Methods ---------------------------------- #
    @classmethod
    def _debug(cls, debug: Optional[bool] = None) -> bool:
        """ Set or get debug mode. (Class method) """
        if debug is not None:
            cls._debug_mode = debug
        return cls._debug_mode

    @classmethod
    def _increase_cached_size(cls, size: int) -> None:
        cls._total_file_size += size

    @classmethod
    def get_files(cls) -> dict[str, Self]:
        """ Get all MediaInfo instances. """
        return cls._files

    # -------------------------------- Init Methods ---------------------------------- #
    def _get_ffprobe(self) -> str | None:
        return shutil.which('ffprobe')

    def _get_raw_data(self) -> dict[str, Any]:
        ffprobe = self._get_ffprobe()
        if not ffprobe:
            raise RuntimeError(
                "ffprobe not found, please make sure you installed ffmpeg correctly."
            )

        # Process the media file
        try:
            # Call ffprobe with JSON output
            result = subprocess.run(
                # [mkvmerge, '-J', file_path],
                [
                    ffprobe,
                    '-v', 'quiet',
                    '-print_format', 'json',
                    '-show_format',
                    '-show_streams',
                    self._file_path,
                ],
                capture_output=True,
                text=True,
                check=True,
            )

        except subprocess.CalledProcessError as e:
            raise QueryError(f"[ERROR] Failed to execute ffprobe: {e}") from e

        except Exception as e:
            print(f"[ERROR] Failed to get raw data from ffprobe: {e}")
            raise

        if not result.stdout:
            raise QueryError("Failed to get raw data from ffprobe.")

        return json.loads(result.stdout)

    def _get_format_data(self) -> FormatData:
        # Read standard info
        _format: dict[str, Any] = self._raw_info.get('format', {})
        _tags: dict[str, Any] = _format.get('tags', {})

        _size: int = int(_format.get('size', 0))
        _duration: float = float(_format.get('duration', 0))
        _format_name: str = _format.get('format_name', 'Unknown')
        _format_long_name: str = _format.get('format_long_name', _format_name)

        self._increase_cached_size(_size)

        return FormatData(
            score=int(_format.get('probe_score', 0)),
            size=_size,
            duration=_duration,
            duration_str=self._convert_duration_to_str(_duration),
            format=_format_name,
            format_long_name=_format_long_name,
            bitrate=int(_format.get('bit_rate', 0)),
            encoder=_tags.get('ENCODER', 'Unknown'),
            encoding_info=_tags.get('ENCODING_INFO', 'Unknown'),
        )

    def _get_tracks_data(self) -> None:
        _tracks: list[dict[str, Any]] = self._raw_info.get('streams', [])
        data: TrackTypes

        for track in _tracks:
            track_type: str = track.get('codec_type', 'Unknown')
            # * video, audio, subtitle, attachment(font, etc.)
            match track_type:
                case 'video':
                    data = self._extract_video_info(track)
                    if data.index is None:
                        print(
                            "[WARNING] A video track didn't have index: "
                            f"{track.get('codec_name', self._file_path)}"
                        )
                        continue
                    if data.index not in self._video_tracks:
                        self._video_tracks[data.index] = data

                case 'audio':
                    data = self._extract_audio_info(track)
                    if data.index is None:
                        print(
                            "[WARNING] An audio track didn't have index: "
                            f"{track.get('codec_name', self._file_path)}"
                        )
                        continue
                    if data.index not in self._audio_tracks:
                        self._audio_tracks[data.index] = data

                case 'subtitle':
                    data = self._extract_subtitle_info(track)
                    if data.index is None:
                        print(
                            "[WARNING] A subtitle track didn't have index: "
                            f"{track.get('codec_name', self._file_path)}"
                        )
                        continue
                    if data.index not in self._subtitle_tracks:
                        self._subtitle_tracks[data.index] = data

                case 'attachment':
                    data = self._extract_attach_info(track)
                    if data.index is None:
                        print(
                            "[WARNING] An attachment track didn't have index: "
                            f"{track.get('codec_name', self._file_path)}"
                        )
                        continue
                    if track.get('codec_name', '') in ['ttf', 'ttc', 'woff', 'woff2']:
                        self._attach_fonts += 1

                    if data.index not in self._attach_tracks:
                        self._attach_tracks[data.index] = data

                case 'Unknown':
                    print(
                        "[WARNING] A track didn't have codec_type: "
                        f"{track.get('codec_name', self._file_path)}"
                    )
                    continue

                case _:
                    print(f"[WARNING] A track can't be identified: {track_type}")
                    continue

            self._tracks[data.index] = track_type

            if track_type not in self._tracks_by_type:
                self._tracks_by_type[track_type] = []
            self._tracks_by_type[track_type].append(data.index)

    # ------------------------------- Track Methods ---------------------------------- #
    def _extract_video_info(self, track: dict[str, Any]) -> VideoTrack:
        _disposition: dict[str, Any] = track.get('disposition', {})
        _tags: dict[str, Any] = track.get('tags', {})

        _display_width: int = track.get('width', 0)
        _display_height: int = track.get('height', 0)
        _pixel_width: int = track.get('coded_width', 0)
        _pixel_height: int = track.get('coded_height', 0)
        _display_dimensions: str = f'{_display_width}x{_display_height}'
        _pixel_dimensions: str = f'{_pixel_width}x{_pixel_height}'

        _duration: str = _tags.get('DURATION', '')
        _duration_sec: float = self._convert_duration_to_sec(_duration)
        _total_frames: int = int(_tags.get('NUMBER_OF_FRAMES', 0))

        # Calculate fps
        if _duration_sec and _total_frames:
            _fps = round(_total_frames / _duration_sec, 5)
        else:
            _fps = 0

        # Map properties information to VideoTrack and return
        return VideoTrack(
            index=track.get('index', None),
            default=_disposition.get('default', False),
            forced=_disposition.get('forced', False),
            codec=track.get('codec_long_name', track.get('codec_name', 'Unknown')),
            language=base.LANGUAGE_CODES.get(
                _tags.get('language', ''),
                'Unknown'
            ),
            duration=_duration,
            duration_sec=_duration_sec,
            fps=_fps,
            bps=_tags.get('BPS', 0),
            display_dimensions=_display_dimensions,
            display_width=_display_width,
            display_height=_display_height,
            display_aspect_ratio=track.get('display_aspect_ratio', 'Unknown'),
            display_resolution=base.VIDEO_RESOLUTION_STANDARDS.get(
                _display_dimensions,
                'Unknown'
            ),
            pixel_width=_pixel_width,
            pixel_height=_pixel_height,
            pixel_dimensions=_pixel_dimensions,
            pixel_format=track.get('pix_fmt', 'Unknown').upper(),
            color_range=track.get('color_range', 'Unknown'),
            color_space=track.get('color_space', 'Unknown'),
            color_transfer=track.get('color_transfer', 'Unknown'),
            color_primaries=track.get('color_primaries', 'Unknown'),
        )

    def _extract_audio_info(self, track: dict[str, Any]) -> AudioTrack:
        # Map properties information to AudioTrack and return
        return AudioTrack(
            index=track.get('index', None),
            codec=track.get('codec_long_name', track.get('codec_name', 'Unknown')),
            channels=track.get('channels', 0),
            sample_rate=track.get('sample_rate', 0),
            language=base.LANGUAGE_CODES.get(
                track.get('language', ''),
                'Unknown'
            ),
            bit_depth=track.get('bits_per_sample', 0),
            duration=track.get('duration', 0),
        )

    def _extract_subtitle_info(self, track: dict[str, Any]) -> SubtitleTrack:
        # Map properties information to SubtitleTrack and return
        return SubtitleTrack(
            index=track.get('index', None),
            codec=track.get('codec_name', 'Unknown'),
            language=base.LANGUAGE_CODES.get(
                track.get('language', ''),
                'Unknown'
            ),
            forced=track.get('disposition', {}).get('forced', False),
            default=track.get('disposition', {}).get('default', False),
            hearing_impaired=track.get(
                'disposition', {}
            ).get('hearing_impaired', False),
            visual_impaired=track.get('disposition', {}).get('visual_impaired', False),
            font_name=track.get('tags', {}).get('filename', 'Unknown'),
            mimetype=track.get('tags', {}).get('mimetype', 'Unknown'),
            duration=track.get('duration', 0),
        )

    def _extract_attach_info(self, track: dict[str, Any]) -> AttachTrack:
        _tags: dict[str, Any] = track.get('tags', {})
        # Map properties information to AttachTrack and return
        return AttachTrack(
            index=track.get('index', None),
            codec=track.get('codec_name', 'Unknown'),
            filename=_tags.get('filename', 'Unknown'),
            mimetype=_tags.get('mimetype', 'Unknown'),
            disposition=track.get('disposition', {}),
        )

    # ------------------------------ Internal Methods -------------------------------- #
    def _convert_duration_to_str(self, duration: float) -> str:
        """ Convert duration from float (seconds) to HH:MM:SS.SSS format. """
        if duration == 0:
            return '00:00:00.000'

        h = int(duration // 3600)
        m = int((duration % 3600) // 60)
        s = duration % 60
        return f'{h:02d}:{m:02d}:{s:06.3f}'

    def _convert_duration_to_sec(self, duration_str: str) -> float:
        """ Convert duration from string (HH:MM:SS.SSS) to float seconds. """
        if not duration_str:
            return 0

        h, m, s = map(float, duration_str.split(':'))
        return h * 3600 + m * 60 + s

    # ------------------------------- Public Methods --------------------------------- #
    def get(self, index: int) -> TrackTypes | None:
        """ Get data from the specific track. """
        track = self._tracks.get(index, '')
        if not track:
            print(f"[WARNING] Track {index} not found in {self._file_path}")
            return None

        track_data = getattr(self, f'_{track}_tracks', {}).get(index, None)
        return track_data

    # ---------------------------- Properties: Internal ------------------------------ #
    @property
    def debug(self) -> bool:
        """ Debug mode status (Class value) """
        return self._debug()

    @debug.setter
    def debug(self, debug: bool) -> bool:
        """ Set debug mode (Will apply to all MediaInfo instances) """
        self._debug(debug)
        return self._debug()

    @property
    def total_cached_size(self) -> int:
        """ Get total size of all media files by bytes (Class value) """
        return self.__class__._total_file_size

    # ------------------------------ Properties: File -------------------------------- #
    @property
    def name(self) -> str:
        """ Get file name of the media file. """
        return self._file_path.name

    @property
    def path(self) -> Path:
        """ Get file path of the media file. """
        return self._file_path

    @property
    def raw(self) -> dict[str, Any]:
        """ Get raw data of the media file. """
        return self._raw_info

    @property
    def tracks(self) -> dict[int, str]:
        """ Get tracks of the media file. """
        return self._tracks

    @property
    def tracks_by_type(self) -> dict[str, list[int]]:
        """ Get tracks by type. """
        return self._tracks_by_type

    @property
    def total_tracks(self) -> int:
        """ Get total tracks of the media file. """
        return len(self._tracks)

    @property
    def total_video_tracks(self) -> int:
        """ Get total video tracks of the media file. """
        return len(self._video_tracks)

    @property
    def total_audio_tracks(self) -> int:
        """ Get total audio tracks of the media file. """
        return len(self._audio_tracks)

    @property
    def total_subtitle_tracks(self) -> int:
        """ Get total subtitle tracks of the media file. """
        return len(self._subtitle_tracks)

    @property
    def total_attach_tracks(self) -> int:
        """ Get total attach tracks of the media file. """
        return len(self._attach_tracks)

    @property
    def total_fonts(self) -> int:
        """ Get total fonts of the media file. """
        return self._attach_fonts

    # --------------------------- Properties: FormatData ----------------------------- #
    @property
    def score(self) -> int:
        """ Get ffprobe score

        The score is a value between 0 and 100, which indicates the confidence of
        the ffprobe in the format and streams.

        The data is for reference only, it may not be accurate.

        It ranges from 0 to 100, with 100 indicating absolute certainty.
        FFmpeg analyzes the file's initial content, assigning scores to potential
        formats.

        Higher scores suggest greater confidence in the format identification.
        This score is particularly useful for detecting mismatches between file
        extensions and actual content, aiding in accurate format determination.
        """
        return self._format_data.score

    @property
    def size(self) -> int:
        """ Get size of the media file. (bytes) """
        return self._format_data.size

    @property
    def size_kb(self) -> str:
        """ Calculate size to human readable format. (KB) """
        return f'{self.size / 1024:.2f} KB'

    @property
    def size_mb(self) -> str:
        """ Calculate size to human readable format. (MB) """
        return f'{self.size / 1024 ** 2:.2f} MB'

    @property
    def size_gb(self) -> str:
        """ Calculate size to human readable format. (GB) """
        return f'{self.size / 1024 ** 3:.2f} GB'

    @property
    def duration(self) -> str:
        """ Get duration of the media file. (HH:MM:SS.SSS) """
        return self._format_data.duration_str

    @property
    def duration_sec(self) -> float:
        """ Get duration of the media file. (seconds) """
        return self._format_data.duration


class MediaInfo(_MediaInfo):
    """ MediaInfo class for media files. """
    __slots__ = (
        'created',
        '_file_path',
        '_raw_info',
        '_format_data',
        '_tracks',
        '_tracks_by_type',
        '_video_tracks',
        '_audio_tracks',
        '_subtitle_tracks',
        '_attach_tracks',
        '_attach_fonts',
    )
