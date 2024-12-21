# core/identify/_base.py
from pathlib import Path
import json

# ISO 639-2
with open(Path(__file__).parent / 'info/ISO_639-2.json', 'r') as f:
    LANGUAGE_CODES = json.load(f)

# =================================== Video Track ==================================== #
VIDEO_RESOLUTION_STANDARDS = {
    # SDTV & EDTV Standards
    '320x240': 'QVGA',           # 4:3, 240p, Quarter VGA
    '352x240': 'SIF',            # 4:3, 240p, Standard Image Format
    '352x288': 'CIF',            # 4:3, 288p, Common Intermediate Format
    '352x480': '480i',           # 4:3, 480i, SD (NTSC interlaced)
    '480x320': 'HVGA',           # 3:2, 320p, Half VGA
    '640x480': '480p',           # 4:3, 480p,  4:3, 480p, VGA (Video Graphics Array)
    '720x480': 'SD_NTSC',        # 4:3/16:9(anamorphic), SD (NTSC)
    '720x576': '576i',           # 4:3/16:9(anamorphic), SD Phase Alternating Line
    '768x576': 'SD_PAL+',        # 4:3, 576p, Standard Definition PAL+
    '854x480': 'FWVGA',          # 16:9, 480p, Full Wide VGA
    '960x540': 'qHD',            # 16:9, 540p, Quarter HD
    '1024x576': '576p',          # 16:9, Wide Super VGA
    '1024x768': 'XGA',           # 4:3/1.33:1, 768p, Extended Graphics Array

    # HDTV Standards
    '960x720': '720p',           # 4:3, 720p, HD Ready
    '1152x648': '720p',          # 16:9, HD Ready
    '1280x720': '720p',          # 16:9, High Definition
    '1280x800': '800p',          # 16:10, 800p, WXGA (Wide XGA)
    '1280x960': '960p',          # 4:3, 960p, High resolution format
    '1280x1080': '1080p',        # 16:9, 1080p Anamorphic format
    '1366x768': '768p',          # 16:9, Wide XGA
    '1440x900': 'WXGA+',         # 16:10, 900p, Wide XGA Plus
    '1440x1080': '1080p',        # 16:9, 1080p Anamorphic format
    '1440x1440': 'Square_HD',    # 1:1, 1440p, Square HD
    '1600x900': '900p',          # 16:9, 900p, HD Plus
    '1600x1200': 'UXGA',         # 4:3, 1200p, Ultra XGA
    '1620x1080': '1080_WIDE',    # 3:2, 1080p Wide format
    '1680x1050': 'WSXGA+',       # 16:10, 1050p, Wide SXGA Plus
    '1920x1080': '1080p',        # 16:9, Full HD
    '1920x1200': '1200p',        # 16:10, 1200p, Wide Ultra XGA
    '2400x1600': 'Full_HD+',     # 16:10, 1600p, Full HD Plus
    '2560x1080': 'UWFHD',        # 21:9, 1080p, Ultra Wide HD
    '3840x1080': 'DFHD',         # 32:9, 1080p, Dual Full HD (Two 1920x1080 sbs)


    # Digital Cinema
    '1920x1440': 'QHD',          # 4:3, 1440p, Quad HD
    '1998x1080': '2K_Flat',      # 1.85:1
    '2048x858': '2K_Scope',      # 2.39:1
    '2048x1080': '2K_DCI',       # 1.90:1
    '2048x1536': '2K_DCI',       # 4:3, 1536p, Digital Cinema Initiatives
    '2560x1440': '1440p',        # 16:9, Wide Quad HD
    '2560x1600': 'WQXGA',        # 16:10, 1600p, Wide Quad HD
    '2560x2048': 'QSXGA',        # 5:4, 2048p, Quad Super Extended Graphics Array
    '2732x1536': 'iPad_Pro',     # 16:9, 1536p, iPad Pro
    '3200x1440': 'WQHD+',        # 16:9, Wide Quad HD Plus
    '3200x1800': 'QHD+',         # 16:9, Quad HD Plus
    '3440x1440': '2K_UWQHD',     # 21:9, 1440p, Ultra Wide Quad HD
    '3840x1600': 'UWQHD+',       # 21:9, 1600p, Ultra Wide Quad HD+
    '3840x2400': '4K WQUXGA',    # 16:10, 2400p, Wide Quad Ultra Extended Graphics Array
    '3996x2160': '4K_Flat',      # 1.85:1
    '4096x1716': '4K_Scope',     # 2.39:1
    '4096x2160': '4K_DCI',       # 1.90:1
    '5120x1440': 'DQHD',         # 32:9, 1440p, Dual Quad HD
    '5120x2880': '5K',           # 16:9, 2880p, 5K
    '5120x3200': '5K',           # 16:10, 3200p, 5K
    '6016x3384': '6K',           # 16:9, 3384p, 6K
    '7680x3200': '8K UWD',       # 21:9, 3200p, 8K Ultra Wide

    # UHDTV Standards (Rec. 2020)
    '3840x2160': '2160p',        # 16:9, 2160p, 4K UHD (Ultra HD)
    '7680x4320': '4320p',        # 16:9, 4320p, 8K UHD (Ultra HD)

    # Film Formats
    '1828x1332': '2K_Academy',   # 1.37:1
    '2880x2160': '3K',           # 4:3, 2160p, 3K
    '3072x2160': '3K',           # 1.42:1, 2160p, 3K
    '3656x2664': '4K_Academy',   # 1.37:1
    '4096x2304': '4K UHD+',      # 16:9, 2304p, 4K UHD+
    '4096x3072': '4K Full',      # 4:3, 3072p, 4K Full Frame
    '5120x2160': '5K',           # 2.37:1, 65mm
    '6144x3160': '6K_IMAX',      # 1.94:1
    '6144x3456': '6K Full',       # 16:9, 3456p, 6K Full Frame
    '8192x3428': '8K_Ultra',     # 2.39:1
    '8192x4320': '8K_Full',      # 1.90:1
    '8192x5460': '8K Full',      # 3:2, 5460p, 8K Full Frame
    '10240x4320': '10K',         # 2.37:1
    '11520x6480': '11K_IMAX',    # 1.78:1, 70mm
}

VIDEO_PIXEL_FORMATS = {
    # YUV Formats
    'yuv420p': 'YUV420P',
    'yuv422p': 'YUV422P',
    'yuv444p': 'YUV444P',
    'yuv410p': 'YUV410P',
    'yuv411p': 'YUV411P',
    'yuvj420p': 'YUVJ420P',
    'yuvj422p': 'YUVJ422P',
    'yuvj444p': 'YUVJ444P',
    'yuv440p': 'YUV440P',
    'yuvj440p': 'YUVJ440P',
    'yuva420p': 'YUVA420P',
    'yuva422p': 'YUVA422P',
    'yuva444p': 'YUVA444P',

    # YUV 16-bit Formats
    'yuv420p16le': 'YUV420P16LE',
    'yuv420p16be': 'YUV420P16BE',
    'yuv422p16le': 'YUV422P16LE',
    'yuv422p16be': 'YUV422P16BE',
    'yuv444p16le': 'YUV444P16LE',
    'yuv444p16be': 'YUV444P16BE',

    # YUV 9/10/12/14-bit Formats
    'yuv420p9be': 'YUV420P9BE',
    'yuv420p9le': 'YUV420P9LE',
    'yuv420p10be': 'YUV420P10BE',
    'yuv420p10le': 'YUV420P10LE',
    'yuv422p10be': 'YUV422P10BE',
    'yuv422p10le': 'YUV422P10LE',
    'yuv444p9be': 'YUV444P9BE',
    'yuv444p9le': 'YUV444P9LE',
    'yuv444p10be': 'YUV444P10BE',
    'yuv444p10le': 'YUV444P10LE',
    'yuv422p9be': 'YUV422P9BE',
    'yuv422p9le': 'YUV422P9LE',
    'yuv420p12be': 'YUV420P12BE',
    'yuv420p12le': 'YUV420P12LE',
    'yuv420p14be': 'YUV420P14BE',
    'yuv420p14le': 'YUV420P14LE',
    'yuv422p12be': 'YUV422P12BE',
    'yuv422p12le': 'YUV422P12LE',
    'yuv422p14be': 'YUV422P14BE',
    'yuv422p14le': 'YUV422P14LE',
    'yuv444p12be': 'YUV444P12BE',
    'yuv444p12le': 'YUV444P12LE',
    'yuv444p14be': 'YUV444P14BE',
    'yuv444p14le': 'YUV444P14LE',

    # RGB Formats
    'rgb24': 'RGB24',
    'bgr24': 'BGR24',
    'rgb48be': 'RGB48BE',
    'rgb48le': 'RGB48LE',
    'rgb565be': 'RGB565BE',
    'rgb565le': 'RGB565LE',
    'rgb555be': 'RGB555BE',
    'rgb555le': 'RGB555LE',
    'rgb444le': 'RGB444LE',
    'rgb444be': 'RGB444BE',
    'rgb8': 'RGB8',
    'rgb4': 'RGB4',
    'rgb4_byte': 'RGB4_BYTE',

    # BGR Formats
    'bgr8': 'BGR8',
    'bgr4': 'BGR4',
    'bgr4_byte': 'BGR4_BYTE',
    'bgr48be': 'BGR48BE',
    'bgr48le': 'BGR48LE',
    'bgr565be': 'BGR565BE',
    'bgr565le': 'BGR565LE',
    'bgr555be': 'BGR555BE',
    'bgr555le': 'BGR555LE',
    'bgr444le': 'BGR444LE',
    'bgr444be': 'BGR444BE',

    # Packed YUV Formats
    'yuyv422': 'YUYV422',
    'uyvy422': 'UYVY422',
    'uyyvyy411': 'UYYVYY411',

    # Planar RGB Formats
    'gbrp': 'GBRP',
    'gbrp9be': 'GBRP9BE',
    'gbrp9le': 'GBRP9LE',
    'gbrp10be': 'GBRP10BE',
    'gbrp10le': 'GBRP10LE',
    'gbrp16be': 'GBRP16BE',
    'gbrp16le': 'GBRP16LE',
    'gbrp12be': 'GBRP12BE',
    'gbrp12le': 'GBRP12LE',
    'gbrp14be': 'GBRP14BE',
    'gbrp14le': 'GBRP14LE',

    # Alpha Formats
    'argb': 'ARGB',
    'rgba': 'RGBA',
    'abgr': 'ABGR',
    'bgra': 'BGRA',
    'rgba64be': 'RGBA64BE',
    'rgba64le': 'RGBA64LE',
    'bgra64be': 'BGRA64BE',
    'bgra64le': 'BGRA64LE',

    # Grayscale Formats
    'gray': 'GRAY',
    'gray16be': 'GRAY16BE',
    'gray16le': 'GRAY16LE',

    # Planar Alpha Formats
    'gray8a': 'GRAY8A',

    # Palette Formats
    'pal8': 'PAL8',

    # Bitstream Formats
    'monow': 'MONOW',
    'monob': 'MONOB',

    # NV12/21 Formats
    'nv12': 'NV12',
    'nv21': 'NV21',

    # 0RGB Formats
    '0rgb': '0RGB',
    'rgb0': 'RGB0',
    '0bgr': '0BGR',
    'bgr0': 'BGR0',
}

MKVMERGE_COLOR_MATRIX_COEFFICIENTS = {
    0: 'Identity/GBR',  # Support GBR(RGB), YZX, sRGB...
    1: 'BT.709',  # HD standard, for Rec.ITU-R BT.709-6, xvYCC709...
    2: 'Unspecified',
    3: 'Reserved',
    4: 'BT.470M',  # US analog TV standard
    5: 'BT.470BG',  # Standard for PAL, SECAM SYSTEM
    6: 'SMPTE 170M',  # Standard for NTSC
    7: 'SMPTE 240M',  # Standard for HDTV
    8: 'YCgCo',  # SMPTE 2085
    9: 'YCgCo-601',  # SMPTE 2085
    10: 'BT.2020',  # HDR standard
}

MKVMERGE_COLOR_PRIMARIES = {
    0: 'Reserved',
    1: 'ITU-R BT.709',
    2: 'Unspecified',
    3: 'Reserved',
    4: 'ITU-R BT.470M',
    5: 'ITU-R BT.470BG',
    6: 'SMPTE 170M',
    7: 'SMPTE 240M',
    8: 'FILM',
    9: 'ITU-R BT.2020',
    10: 'SMPTE ST 428-1',
    22: 'JEDEC P22 phosphors',
}

MKVMERGE_COLOR_RANGE = {
    0: 'unspecified',
    1: 'broadcast range',
    2: 'full range (no clipping)',
    3: 'defined by MatrixCoefficients/TransferCharacteristics',
}

MKVMERGE_COLOR_TRANSFER = {
    0: 'reserved',
    1: 'ITU-R BT.709',
    2: 'unspecified',
    3: 'reserved',
    4: 'gamma 2.2 curve',
    5: 'gamma 2.8 curve',
    6: 'SMPTE 170M',
    7: 'SMPTE 240M',
    8: 'linear',
    9: 'log',
    10: 'log sqrt',
    11: 'IEC 61966-2-4',
    12: 'ITU-R BT.1361 extended color gamut',
    13: 'IEC 61966-2-1',
    14: 'ITU-R BT.2020 10 bit',
    15: 'ITU-R BT.2020 12 bit',
    16: 'SMPTE ST 2084',
    17: 'SMPTE ST 428-1',
    18: 'ARIB STD-B67 (HLG)',
}

# =================================== Audio Track ==================================== #

# ================================== Subtitle Track ================================== #

# ================================== Chapter Track =================================== #
