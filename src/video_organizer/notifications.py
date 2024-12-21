# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

"""
Sayuri's Video Organizer - Notifications

This part is for user notifications.

This's not supposed called from outside the package, you should have your own
stdout/stderr system in your project.

""" # (src) notifications.py

from argparse import Namespace


def warn_ignored_args(parse: str, args: Namespace, ignores: list[str]) -> None:
    """Print warning messages for ignored arguments."""
    ignored_args = []
    for ignore in ignores:
        if getattr(args, ignore):
            ignored_args.append(ignore)

    if ignored_args:
        count = len(ignored_args)
        form = 'an argument was' if count == 1 else f'{count} arguments were'
        print(
            f"[WARNING] There's {form} ignored when `--{parse}` using:\n"
            f"{', '.join(f'--{arg.replace("_", "-")}' for arg in ignored_args)}\n"
        )


# ------------------------------------ Info Print ------------------------------------ #
def notice_search_options(
    includes: tuple[str, ...],
    excludes: tuple[str, ...],
    extensions: tuple[str, ...],
) -> None:
    """Print the current file matching options."""
    # Print current options
    if any([includes, excludes, extensions]):
        print('- with options:')
        if includes:
            print(f"  - including: {includes}")
        if excludes:
            print(f"  - excluding: {excludes}")
        if extensions:
            print(f"  - extensions: {extensions}")
        print()


def notice_found_files(count: int) -> None:
    """Print the number of files found."""
    match count:
        case 0:
            print("No file found.")
        case 1:
            print("Found 1 file.")
        case _:
            print(f"Found {count} files.")
