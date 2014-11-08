# -*- coding: utf-8 -*-
#
# (C) Janusz Kowalczyk (kowalcj0) 2014

from mock import MagicMock, patch

from dinky.controllers.roothandler import RootHandler

from tornado.escape import json_encode


@patch('dinky.controllers.roothandler.options')
@patch('tornado.process')
def test_get_service_status(process, options):
    options.version = '0.1.0'
    root = RootHandler(MagicMock(), MagicMock())
    root.write = MagicMock()

    process.task_id = MagicMock(return_value=0)

    # MUT
    root.get()
    msg = {"service_name": 
           "dinky - send docs to kindle service",
           "version": "{}".format(options.version)}

    root.write.assert_called_once_with(json_encode(msg))
