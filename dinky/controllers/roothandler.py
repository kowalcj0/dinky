# -*- coding: utf-8 -*-
# (C) Janusz Kowalczyk (kowalcj0) 2014
"""API Root handler. Return basic information about the service.
"""

import tornado.web
from tornado.options import options
from tornado.escape import json_encode


class RootHandler(tornado.web.RequestHandler):
    """Responsible for providing basic inf. on the service, like:
    + its name
    + current minor version
    """

    def get(self):
        """Respond with JSON containing service name and current minor version
        of the service.
        """
        msg = {"service_name": 
               "dinky - send docs to kindle service",
               "version": "{}".format(options.version)}

        self.write(json_encode(msg))
