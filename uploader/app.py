
import os

from tornado.web import Application
from tornado.web import StaticFileHandler

from uploader.handlers import IndexHandler
from uploader.handlers import UploadHandler
from uploader.handlers import UploadProgressHandler


def create_app(root_dir, debug=False):
    settings = {
        'template_path': os.path.join(root_dir, 'templates'),
        'debug': debug,
        'static_path': os.path.join(root_dir, 'static'),
        'static_url_prefix': '/static/',
        'static_hash_cache': debug,
        'uploaded_dir': os.path.join(root_dir, 'uploaded'),
    }

    mapping = [
        (r'/', IndexHandler),
        (r'/upload', UploadHandler),
        (r'/progress', UploadProgressHandler),
        (r'/static/(.*)', StaticFileHandler),
        (r'/uploaded/(.*)', StaticFileHandler, {
            'path': os.path.join(root_dir, 'uploaded')
        })
    ]

    return Application(mapping, **settings)
