# coding: utf-8

from __future__ import absolute_import, division, print_function, with_statement

import os
import json

from tornado.web import RequestHandler
from tornado.web import stream_request_body
from tornado import gen
from tornado.log import gen_log

from uploader.post_streamer import PostDataStreamer


class MyPostDataStreamer(PostDataStreamer):
    percent = 0

    def on_progress(self):
        if self.total:
            percent = self.received * 100 // self.total
            if percent != self.percent:
                self.percent = percent


class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


@stream_request_body
class UploadHandler(RequestHandler):
    def prepare(self):
        _id = self.get_query_argument('id')
        content_length = self.request.headers.get('Content-Length', '0')

        try:
            total = int(content_length)
        except ValueError:
            total = 0

        self.parser = MyPostDataStreamer(total)

        gen_log.debug('#{_id}: init upload request.'.format(_id=_id))

    @gen.coroutine
    def data_received(self, data):
        _id = self.get_query_argument('id')

        gen_log.debug('#{_id}: received {size} byte(s).'.format(
            _id=_id, size=len(data)
        ))

        self.application.storage[_id] = self.parser.percent

        self.parser.receive(data)

        yield gen.sleep(0.01)

    def post(self):
        """
        Upload file
        """
        _id = self.get_query_argument('id')
        uploaded_dir = self.application.settings['uploaded_dir']
        buf_size = 4096

        try:
            self.parser.finish_receive()

            for part in self.parser.parts:
                filename = part['headers'][0]['params']['filename']
                tmpfile = part['tmpfile']

                full_path = os.path.join(uploaded_dir, filename)

                with open(full_path, 'wb') as fp:
                    tmpfile.seek(0)
                    while True:
                        buf = tmpfile.read(buf_size)
                        if not buf:
                            break
                        fp.write(buf)

            self.set_header('Content-type', 'text/plain; charset=UTF-8')
            self.write(json.dumps({
                'id': _id,
                'status': 'complete',
                'download_url': u'/uploaded/{}'.format(filename)
            }))
            self.finish()
        finally:
            self.parser.release_parts()

        gen_log.debug('#{_id}: upload complete.'.format(_id=_id))

    def on_finish(self):
        _id = self.get_query_argument('id')

        try:
            del self.application.storage[_id]
        except KeyError:
            pass

        gen_log.debug('#{_id}: cleanup.'.format(_id=_id))


class UploadProgressHandler(RequestHandler):
    def get(self):
        """
        Return file upload progress
        """
        _id = self.get_query_argument('id')

        gen_log.debug('#{_id}: progress request.'.format(_id=_id))

        try:
            progress = self.application.storage[_id]

            self.write({
                'id': _id,
                'progress': progress,
            })
        except KeyError:
            self.send_error(404)
