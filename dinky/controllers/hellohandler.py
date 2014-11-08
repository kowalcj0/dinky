# -*- coding: utf-8 -*-
# (C) Janusz Kowalczyk (kowalcj0) 2014
"""API hello handler. Returns hello world when endpoint hit.
"""
import logging

import tornado.web
from tornado.options import options
from tornado.escape import json_encode


class HelloHandler(tornado.web.RequestHandler):
    """Responsible for providing basic inf. on the service, like:
    + its name
    + current minor version
    """

    def get(self):
        """Respond with JSON containing service name and current minor version
        of the service.
        """
        msg = {"service_name":
               "Dinky - send docs to kindle service",
               "message":"Hello World",
               "version": "{}".format(options.version)}
        logging.info("send back msg %s", msg)
        self.write(json_encode(msg))
