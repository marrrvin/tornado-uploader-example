
import os

from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.options import define
from tornado.options import parse_command_line

from uploader.app import create_app

CURRENT_DIR = os.path.dirname(__file__)

DEFAULT_PORT = 8888

DEFAULT_UPLOADED_DIR = os.path.join(CURRENT_DIR, 'uploaded')


define(
    'debug',
    type=bool,
    default=False,
    help='Enable debug mode'
)
define(
    'port',
    type=int,
    default=DEFAULT_PORT,
    help='Application port'
)
define(
    'uploaded_dir',
    default=DEFAULT_UPLOADED_DIR,
    help='Directory for uploaded files'
)


def main():
    """
    Entry point
    """
    parse_command_line()

    app = create_app(
        CURRENT_DIR,
        debug=options.debug,
        uploaded_dir=options.uploaded_dir
    )
    app.listen(options.port)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
