#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv

from gevent import monkey
monkey.patch_all()

import bottle
from bottle import default_app, request, route, response, get

bottle.debug(True)


@get('/')
def index():
    response.content_type = 'text/plain; charset=utf-8'
    ret = 'Hello world, I\'m %s!\n\n' % os.getpid()
    ret += 'Request vars:\n'
    for k, v in list(iter(request.environ.items())):
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += '\n'
    ret += 'Environment vars:\n'

    for k, v in list(iter(env.items())):
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    return ret


# bottle.run(server='gevent', port=os.environ.get('PORT', 5000))
bottle.run(host='0.0.0.0', port=5000)
