import sys
from argparse import ArgumentParser

import uvicorn

from bushido import __version__

from bushido.core.conf import DEFAULT_PORT


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description='bushido server')
    parser.add_argument('--version', action='store_true', help='show version')
    parser.add_argument(
        '--devel', action='store_true', help='run development server'
    )
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        print(f'bushido v{__version__}')
        sys.exit(0)

    if args.devel:
        uvicorn.run(
            'bushido.main:create_app',
            port=DEFAULT_PORT,
            reload=True,
            factory=True,
            log_level='debug',
        )
    else:
        uvicorn.run(
            'bushido.main:create_app',
            port=DEFAULT_PORT,
            factory=True,
            log_level='info',
        )


if __name__ == '__main__':
    main()
