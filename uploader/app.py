# coding: utf-8

import os

from tornado.web import Application
from tornado.web import StaticFileHandler

from uploader.handlers import IndexHandler
from uploader.handlers import UploadHandler
from uploader.handlers import UploadProgressHandler


def create_app(root_dir=None, debug=False, uploaded_dir=None):
    """
    Application factory.

    :param root_dir: path to application directory
    :param debug: debug mode flag
    :param uploaded_dir: path to uploaded files directory

    :return: new application instance
    """
    settings = {
        'template_path': os.path.join(root_dir, 'templates'),
        'debug': debug,
        'static_path': os.path.join(root_dir, 'static'),
        'static_url_prefix': '/static/',
        'static_hash_cache': debug,
        'uploaded_dir': uploaded_dir
    }

    mapping = [
        (r'/', IndexHandler),
        (r'/upload', UploadHandler),
        (r'/progress', UploadProgressHandler),
        (r'/static/(.*)', StaticFileHandler),
        (r'/uploaded/(.*)', StaticFileHandler, {
            'path': uploaded_dir
        })
    ]

    return Application(mapping, **settings)
