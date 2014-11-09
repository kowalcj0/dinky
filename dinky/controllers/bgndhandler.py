# -*- coding: utf-8 -*-
# (C) Janusz Kowalczyk (kowalcj0) 2014
"""API background handler. Runs task in background and returns to the caller.
read more here:
http://www.tornadoweb.org/en/stable/ioloop.html#tornado.ioloop.IOLoop.spawn_callback
https://gist.github.com/methane/2185380
"""
import logging

import tornado.web
from tornado.options import options
from tornado.escape import json_encode
from tornado.ioloop import IOLoop
import time
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor   # 'pip install futures' for python2

MAX_WORKERS = 4


class BgndHandler(tornado.web.RequestHandler):
    """Run a background task without blocking the caller
    """
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @run_on_executor
    def background_task(self):
        """ This will be executed in 'executor' pool. """
        logging.info("sleeping for 5s")
        time.sleep(5)
        return True

    @tornado.gen.coroutine
    def get(self):
        """ Request that asynchronously calls background task. """
        res = self.background_task()
        self.finish(b'background')
