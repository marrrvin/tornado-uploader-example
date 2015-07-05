
import os

from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.options import define
from tornado.options import parse_command_line

from uploader.app import create_app

DEFAULT_PORT = 8888

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


def main():
    parse_command_line()

    current_dir = os.path.dirname(__file__)

    application = create_app(current_dir, debug=options.debug)
    application.listen(options.port)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
