# -*- coding: utf-8 -*-
#
# (C) Janusz Kowalczyk (kowalcj0) 2014
#
"""
Python Behave configuration file

Start the Dinky service up before running all the tests.

"""


import logging
import os
import subprocess
import signal
import time
import requests

REPORT_DIR = os.path.join(os.path.dirname(__file__), '../reports')
ROOT_DIR = os.path.join(os.path.dirname(__file__), '../../..')
API_MOCK = os.environ.get('API_MOCK')

if API_MOCK:
    BASE_URL = API_MOCK
else:
    BASE_URL = 'http://127.0.0.1:8000'
API_VERSION = "v0"
API_NAME = "dinky"


def before_scenario(context, scenario):
    """Any instructions executed before every scenario
    """
    pass


def after_scenario(context, scenario):
    """Any instructions executed after every scenario
    """
    pass


def after_all(context):
    """Any instructions executed after all scenarios were executed
    """
    _kill_server(context.server_process)


def before_all(context):
    """
    Executes the code before all the tests are run
    """

    context.log = _setup_logging()
    if API_MOCK:
        context.server_process = None
        context.api_mock = True
    else:
        context.server_process = _start_server()
        context.api_mock = False
        context.aborted = not _ping_server()

    context.endpoint = lambda resource: '{}/{}/{}{}'.format(
        BASE_URL, API_VERSION, API_NAME, resource)


def _start_server():
    """
    start the server in a subprocess
    """
    print "Starting up the server..."
    server_process = subprocess.Popen(
        "nohup python {}/dinky/ >>{}/runserver.log 2>&1 &".format(
            ROOT_DIR, REPORT_DIR), shell=True, preexec_fn=os.setsid)
    return server_process


def _ping_server(timeout=5):
    """
    ping the server with a timeout
    """
    step = 0.5
    while True:
        time.sleep(step)
        try:
            requests.get(BASE_URL, timeout=step)
            print "Server is up"
            return True
        except Exception:
            timeout -= step
            if timeout < 0:
                print('server failed to start')
                break
    return False


def _kill_server(server_process):
    """
    kill the server subprocess group
    """
    if server_process:
        print "\nKilling the stale instance of a server..."
        os.killpg(server_process.pid, signal.SIGTERM)


def _setup_logging():
    """
    set up the logging facility
    """
    # get logger
    log = logging.getLogger('template_service.Behave')
    # create file handler which logs even debug messages
    # overwrite the old log file
    fh = logging.FileHandler(
        filename='{}/behave-debug.log'.format(REPORT_DIR), mode='w')
    # create console handler with a higher log level
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        '%a %Y-%m-%d %H:%M:%S %z')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    log.addHandler(ch)
    log.addHandler(fh)
    # if not context.config.log_capture:
    # logging.basicConfig(level=logging.DEBUG)
    return log
