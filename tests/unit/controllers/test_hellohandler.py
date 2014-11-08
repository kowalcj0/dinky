# -*- coding: utf-8 -*-
#
# (C) Janusz Kowalczyk (kowalcj0) 2014

from mock import MagicMock, patch

from dinky.controllers.hellohandler import HelloHandler

from tornado.escape import json_encode


@patch('dinky.controllers.hellohandler.options')
@patch('tornado.process')
def test_get_service_status(process, options):
    options.version = '0.1.0'
    hello = HelloHandler(MagicMock(), MagicMock())
    hello.write = MagicMock()

    process.task_id = MagicMock(return_value=0)

    # MUT
    hello.get()
    msg = {"service_name": 
           "Dinky - send docs to kindle service",
           "message":"Hello World",
           "version": "{}".format(options.version)}

    hello.write.assert_called_once_with(json_encode(msg))
