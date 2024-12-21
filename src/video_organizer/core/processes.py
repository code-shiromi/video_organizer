# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

"""
Sayuri's Video Organizer - Requests processing

This part is for processing requests.

This's the way you can call the process from outside the package.

For more information, see documentation.

# ! Not finished yet.

""" # (src) core/processes.py

from .. import (
    notice,
    Config,
)

from pathlib import Path

from ._process_media import MediaProcessor


# ==================================== Entry Point =================================== #
def process(config: Config) -> bool:
    """Process the arguments"""
    args = config.args
    path = config.path

    if not config.quiet:
        process_dir = "Current directory" if path == Path('.') else path
        print(f"Processing directory: {process_dir}\n")

    if args.info:
        if config.debug or not config.quiet:
            notice.warn_ignored_args('info', args, ['save'])

        info = MediaProcessor(config).data

        print(info)

    else:
        print(config.parser.print_help())

    return True
