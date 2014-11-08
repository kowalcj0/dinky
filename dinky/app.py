# -*- coding: utf-8 -*-
# (C) Janusz Kowalczyk (kowalcj0) 2014
"""Configures and starts up the Dinky Service.
"""
import logging
from logging.handlers import SysLogHandler
import os.path
import socket

import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
from tornado.util import exec_in
from tornado.escape import native_str
from tornado.web import RedirectHandler

from dinky.controllers import roothandler, hellohandler

# directory containing the config files
CONF_DIR = os.path.join(os.path.dirname(__file__), '../config')


def configure_syslog():
    """
    Configure syslog logging channel.
    It is turned on by setting `syslog_host` in the config file.
    The port default to 514 can be overridden by setting `syslog_port`.
    """
    syslog_host = getattr(options, 'syslog_host', None)
    if syslog_host:
        handler = SysLogHandler(address=(syslog_host,
                                         options.syslog_port))

        ip = socket.gethostbyname(socket.gethostname())
        formatter = logging.Formatter(ip+' '+options.name + ' %(message)s')
        handler.setFormatter(formatter)

        logging.getLogger().addHandler(handler)


def define_options():
    """
    Define the options from default.conf dynamically
    """
    default = {}
    with open(os.path.join(CONF_DIR, 'default.conf'), 'rb') as f:
        exec_in(native_str(f.read()), {}, default)

    for name, value in default.iteritems():
        # if the option is already defined by tornado
        # override the value
        # a list of options set by tornado:
        # log_file_num_backups, logging, help,
        # log_to_stderr, log_file_max_size, log_file_prefix
        if name in options:
            setattr(options, name, value)
        # otherwise define the option
        else:
            define(name, value)


def load_config():
    """
    Use default.conf as the definition of options with default values
    using tornado.options.define.
    Then overrides the values from: local.conf.
    This mapping allows to access the application configuration across the
    application.

    NOTE:
    logging in load_config() is not going to work because logging is
    configured only when tornado.options.parse_command_line(final=True)
    """
    define_options()
    local_conf = os.path.join(CONF_DIR, 'local.conf')
    if os.path.isfile(local_conf):
        options.parse_config_file(local_conf, final=False)


def log_config():
    """Logs the config used to start the application
    """
    logging.info('Service will be started with such settings:')
    for o in options.as_dict():
        logging.info("{}=\"{}\"".format(o, options.as_dict()[o]))


def setup_server():
    """
    Loads the routes and starts the server
    """

    version_url_prefix = 'v{}'.format(options.version.split('.')[0])

    application = tornado.web.Application([
        (r"/", RedirectHandler, {"url":
                                 r"/{}/dinky".format(version_url_prefix)}),
        (r"/{}/dinky".format(version_url_prefix), roothandler.RootHandler),
        (r"/{}/dinky/hello".format(version_url_prefix),
         hellohandler.HelloHandler)
    ])
    server = tornado.httpserver.HTTPServer(application)

    server.bind(options.port, options.ip)

    # Forks multiple sub-processes, one for each core
    server.start(int(options.processes))

    logging.info('start tornado http server at http://{0}:{1}'.format(
        options.ip, options.port))

    tornado.ioloop.IOLoop.instance().start()


def main():
    """
    The entry point for the Dinky service.
    This will load the configuration files and start a Tornado webservice
    with one or more sub processes.

    NOTES:
    tornado.options.parse_command_line(final=True)
    Allows you to run the service with custom options.
    Examples:
        Change the logging level to debug:
        python dinky --logging=DEBUG
        python dinky --logging=debug

        Configure custom syslog server
        python dinky --syslog_host=54.77.151.169
    """
    load_config()
    tornado.options.parse_command_line(final=True)
    log_config()
    configure_syslog()
    setup_server()


if __name__ == '__main__':      # pragma: no cover
    main()                      # pragma: no cover
