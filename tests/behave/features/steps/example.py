# -*- coding: utf-8 -*-
#
# (C) Janusz Kowalczyk (kowalcj0) 2014
#
import requests

"""Steps implementation for the Dinky service
"""


@given(u'I have the root url of the service')
def step_impl(context):
    assert True


@when(u'I request the root url')
def step_impl(context):
    endpoint = context.endpoint('')
    headers = {'Accept': 'application/json'}
    context.response = requests.get(endpoint, headers=headers)


@then(u'I should get the service information')
def step_impl(context):
    rsp = context.response
    assert rsp.status_code == 200,\
        "Expected 200, got {}. Content:\n{}".format(rsp.status_code,
                                                    rsp.content[:255])
    service_name = rsp.json()['service_name']
    assert service_name == 'dinky - send docs to kindle service',\
           ("Expected "
            "'dinky - send docs to kindle service' got '{}'".format(service_name))


@given(u'I have the hello world url of the service')
def step_impl(context):
    assert True


@when(u'I request the hello world url')
def step_impl(context):
    endpoint = context.endpoint('/hello')
    headers = {
        'Accept': 'application/json'
        }
    context.response = requests.get(endpoint, headers=headers)


@then(u'I should get "Hello World"')
def step_impl(context):
    rsp = context.response
    message = rsp.json()['message']
    assert message == 'Hello World',\
           "Expected 'Hello World' got '{}'".format(message)


@given(u'I have an end point that does not exists')
def step_impl(context):
    assert True


@when(u'I request that not existent url')
def step_impl(context):
    endpoint = context.endpoint('doesnotexist')
    headers = {
        'Accept': 'application/json'
        }
    context.response = requests.get(endpoint, headers=headers)


@then(u'I should get a response with status code 404')
def step_impl(context):
    rsp = context.response
    assert rsp.status_code == 404,\
        "Expected 404, got {}. Content:\n{}".format(rsp.status_code,
                                                    rsp.content[:255])
