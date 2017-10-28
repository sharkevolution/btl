#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import gmail
from gmail import Message


def send_mail(base_mail, base_mailpass, to_mail):

    b = "".join(["sharkevo <", base_mail, ">"])

    gm = gmail.GMail(b, base_mailpass)
    msg = Message('Test Message', to="me <{0}>".format(to_mail), text='Hello')
    gm.send(msg)


def send_mail_key(base_mail, base_mailpass, to_mail, akey):

    b = "".join(["sharkevo <", base_mail, ">"])
    txt = "".join(["Для завершения регистрации и начала работы ",
                   "введите указанный код активации на сайте: ",
                   akey])

    gm = gmail.GMail(b, base_mailpass)
    msg = Message('Завершение регистрации', to="me <{0}>".format(to_mail), text=txt)
    gm.send(msg)