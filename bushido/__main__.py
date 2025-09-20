import sys
import argparse
import uvicorn

# project imports
from bushido.core.conf import DEFAULT_PORT
from bushido import __version__


def create_argparser():
    parser = argparse.ArgumentParser(description='bushido server')
    parser.add_argument('--version', action='store_true', help='show version')
    parser.add_argument('--devel', action='store_true', help='run development server')
    return parser


def main():
    parser = create_argparser()
    args = parser.parse_args()
    if args.version:
        print(f'bushido v{__version__}')
        sys.exit(0)

    if args.devel:
        uvicorn.run('bushido.main:create_app',
                    port=DEFAULT_PORT,
                    reload=True,
                    factory=True,
                    log_level='debug')
    else:
        uvicorn.run('bushido.main:create_app',
                    port=DEFAULT_PORT,
                    factory=True,
                    log_level='info')


if __name__ == '__main__':
    main()
