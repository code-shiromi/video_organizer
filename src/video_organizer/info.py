# ===== Sayuri Gadgets ===== #
# Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)

""" The information module for Uniterm.
This part used in setup scripts like `update_setup.py` and `config.py`.

Change this file when any information about the project is changed.
""" # (src) info.py

import os
import re
import subprocess

_project = 'video-organizer'
_description = (
    "A python video organizer for reading video encode information and "
    "organizing the entire folder."
)
_python_version = '3.12'
_source_dir = 'src/video_organizer'
_docs_dir = 'docs/'

_status = 'Development'
_version = '0.1.0'

_homepage = 'https://shiromi.world'
_repository = 'https://github.com/code-shiromi/video_organizer'
_keywords = [
    'media',
    'video',
    'organizer',
    'mkv',
    'mp4',
    'avi',
    'mov',
    'wmv',
    'flv',
    'webm',
    'm4v',
]

_license = 'MIT'
_copyright = 'Copyright (c) 2024 - 2025 463 Laboratory & Manose K. Y. Carver (Shiromi)'
_author = 'Manose K. Y. Carver (Shiromi)'
_email = 'catch@463.fish'

_credits = ['Mayonetsuki']


def get_version() -> str | None:
    if os.path.isdir('.git'):
        try:
            tags = subprocess.check_output(
                ['git', 'tag'],
                stderr=subprocess.STDOUT
            ).decode().splitlines()

            reg = re.compile(
                r'^v?(?P<version>'
                r'(?P<major>0|[1-9]\d*)\.'
                r'(?P<minor>0|[1-9]\d*)\.'
                r'(?P<patch>0|[1-9]\d*)'
                r'(-(?P<prerelease>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?'
                r'(\+(?P<build>[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?)$'
            )

            valid = [ver.group(1) for tag in tags if (ver := reg.match(tag))]

            if valid:
                def version_key(version):
                    parts = re.split(r'[.-]', version)
                    prerelease = len(parts) > 3
                    return tuple(map(int, parts[:3])), prerelease

                return sorted(valid, key=version_key)[-1]
        except (
            FileNotFoundError,
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired
        ):
            pass
        except Exception as e:
            print(f'Error getting version: {e}')

    return None


git_version = get_version()
if git_version:
    _version = git_version

if __name__ == '__main__':
    print(f'{_project} Information:')
    print(f'{_description}\n')
    print(f'Keywords: {", ".join(_keywords)}\n')
    print(f'Supported Python Version: {_python_version}')
    print(f'Source Directory: {_source_dir}')
    print(f'Documentation Directory: {_docs_dir}')
    print(f'Version: {_version}')
    print(f'Status: {_status}\n')
    print(f'License: {_license}')
    print(f'Copyright: {_copyright}')
    print(f'Author: {_author}')
    print(f'Email: {_email}')
    if _credits:
        print('---')
        print(f'Credits: {", ".join(_credits)}')
    print('---')
    print(f'Homepage: {_homepage}')
    print(f'Repository: {_repository}')
