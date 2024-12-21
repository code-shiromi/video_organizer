# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

"""
Sayuri's Video Organizer

Here's an entry way to directly run the program.

Supposed to be used as a commandline tool with command `video-organizer <options>`.

For more information, see documentation.

Enjoy~

""" # (src) main.py

from . import (
    info,
    notice,
    Config,
)

__version__ = info._version

import sys
from argparse import Namespace

from .core import process

from collections.abc import Sequence


# =================================== Main Function ================================== #
def main(internal_args: Sequence[str] | None = None) -> Namespace:
    """Main function"""
    print("Initializing...\n")

    # ---------------------------------- Process ------------------------------------- #
    config = Config(internal_args)

    args = config.args

    # Initialize global variables
    if config.debug:
        print('[DEBUG MODE: ON]')
        notice.warn_ignored_args('debug', args, ['quiet', 'quiet_flow'])

    if config.quiet:
        notice.warn_ignored_args('quiet', args, ['quiet_flow'])

    if config.quiet_flow:
        notice.warn_ignored_args('quiet_flow', args, ['quiet'])

    if config.info:
        notice.warn_ignored_args('info', args, ['save', 'output'])

    if config.save:
        notice.warn_ignored_args('save', args, ['output', 'info'])

    if config.output:
        notice.warn_ignored_args('output', args, ['save', 'info'])

    try:
        process(config)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    return args  # * for tests


# =================================== Entry Point ==================================== #
def run() -> None:
    """Commandline interface"""
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()
