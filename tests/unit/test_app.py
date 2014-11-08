# -*- coding: utf-8 -*-
# (C) Janusz Kowalczyk (kowalcj0) 2014
import logging
import os.path
from textwrap import dedent

from mock import MagicMock, patch

import dinky.app


@patch('dinky.app.tornado.options')
@patch('dinky.app.setup_server')
@patch('dinky.app.configure_syslog')
@patch('dinky.app.log_config')
@patch('dinky.app.load_config')
def test_main_configure_and_run_service(load_config,
                                        log_config,
                                        configure_syslog,
                                        setup_server,
                                        options):
    # MUT
    dinky.app.main()

    load_config.assert_called_once()
    options.parse_command_line.assert_called_once()
    log_config.assert_called_once()
    configure_syslog.assert_called_once()
    setup_server.assert_called_once()


@patch('dinky.app.options')
@patch('tornado.ioloop.IOLoop.instance')
@patch('tornado.httpserver.HTTPServer')
@patch('tornado.web.Application')
def test_setup_server_binds_to_configured_port(app_class,
                                               server_class,
                                               ioloop,
                                               options):
    options.port = 1234
    options.ip = '0.0.0.0'
    server = MagicMock()
    server_class.return_value = server

    # MUT
    dinky.app.setup_server()

    server.bind.assert_called_once_with(1234, '0.0.0.0')


@patch('dinky.app.options')
@patch('tornado.ioloop.IOLoop.instance')
@patch('tornado.httpserver.HTTPServer')
@patch('tornado.web.Application')
def test_setup_server_starts_server(app_class, server_class, ioloop, options):
    options.version = '0.1.0'
    options.ip = '0.0.0.0'
    options.port = '1234'
    server = MagicMock()
    server_class.return_value = server

    # MUT
    dinky.app.setup_server()

    server.start.assert_called_once()


@patch('dinky.app.options')
@patch('tornado.ioloop.IOLoop.instance')
@patch('tornado.httpserver.HTTPServer')
@patch('tornado.web.Application')
def test_setup_server_starts_server_in_ioloop(app_class,
                                              server_class,
                                              ioloop,
                                              options):
    options.version = '0.1.0'
    options.ip = '0.0.0.0'
    options.port = '1234'
    loop = MagicMock()
    ioloop.return_value = loop

    # MUT
    dinky.app.setup_server()

    loop.start.assert_called_once()


@patch('dinky.app.options')
@patch('tornado.ioloop.IOLoop.instance')
@patch('tornado.httpserver.HTTPServer')
@patch('tornado.web.Application')
def test_setup_server_starts_application_correctly(app_class,
                                                   server_class,
                                                   ioloop,
                                                   options):
    options.version = '0.1.0'
    options.ip = '0.0.0.0'
    options.port = '1234'
    server = MagicMock()
    server_class.return_value = server

    # MUT
    dinky.app.setup_server()

    # assertions follow the execution order
    server_class.called_once_with(app_class)
    server.bind.assert_called_once_with(options.port,
                                        options.ip)
    server.start.assert_called_once_with(int(options.processes))
    server_class.start.assert_called_once()


@patch('dinky.app.tornado.options.options')
@patch('dinky.app.load_config')
@patch('dinky.app.define_options')
@patch('os.path.isfile')
def test_load_config_no_local_config(isfile,
                                     define_options,
                                     load_config,
                                     options):
    isfile.return_value = False

    # MUT
    dinky.app.load_config()
    define_options.assert_called_once()
    load_config.assert_not_called()
    options.run_parse_callbacks.assert_called_once()


@patch('dinky.app.define_options')
@patch('dinky.app.options')
@patch('os.path.isfile')
def test_load_config_local_config(isfile, options, *args):
    isfile.return_value = True
    local_conf_file = os.path.join(dinky.app.CONF_DIR, 'local.conf')

    # MUT
    dinky.app.load_config()
    options.parse_config_file.assert_called_once_with(local_conf_file,
                                                      final=False)


@patch('dinky.app.open', create=True)
def test_define_options(mock_open):
    conf = """
    server = 'localhost'
    port = 8000
    version = '0.0.1'
    """
    file_handle = mock_open.return_value.__enter__.return_value
    file_handle.read = MagicMock(return_value=dedent(conf).strip())

    dinky.app.define_options()
    options = dinky.app.options

    assert options.server == 'localhost'
    assert options.port == 8000
    assert options.version == '0.0.1'


@patch('dinky.app.define')
@patch('dinky.app.open', create=True)
def test_setting_value_for_tornado_predefined_options(mock_open, define):
    conf = """
    log_file_prefix = 'app.log'
    """
    file_handle = mock_open.return_value.__enter__.return_value
    file_handle.read = MagicMock(return_value=dedent(conf).strip())

    dinky.app.define_options()
    options = dinky.app.options

    assert options.log_file_prefix == 'app.log'
    assert define.not_called()


@patch('dinky.app.options')
def test_syslog_on(options):
    options.syslog_host = 'localhost'
    logger = logging.getLogger()
    logger.handlers = []
    dinky.app.configure_syslog()
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], dinky.app.SysLogHandler)


@patch('dinky.app.options')
def test_syslog_off(options):
    options.syslog_host = ''
    logger = logging.getLogger()
    logger.handlers = []
    dinky.app.configure_syslog()
    assert not logger.handlers


@patch('dinky.app.options')
def test_log_config_returns_options_properly(options):
    options.as_dict.return_value = {"example_option": 'example_value'}

    # MUT
    dinky.app.log_config()

    options.as_dict.assert_called_once()


@patch('dinky.app.logging')
@patch('dinky.app.options')
def test_log_config_logs_options_properly(options, logging):
    options.as_dict.return_value = {"example_option": 'example_value'}

    # MUT
    dinky.app.log_config()

    options.as_dict.assert_called_once()
    assert logging.info.call_count == 2
