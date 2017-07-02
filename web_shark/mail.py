#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import psycopg2

import gmail
from gmail import Message


def send_mail(base_mail, base_mailpass, to_mail):

    b = "".join(["sharkevo <", base_mail, ">"])

    gm = gmail.GMail(b, base_mailpass)
    msg = Message('Test Message', to="me <{0}>".format(to_mail), text='Hello')
    gm.send(msg)
