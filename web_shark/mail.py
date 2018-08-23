#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging
import smtplib
from email.message import EmailMessage

import gmail
from gmail import Message

logger = config.main_log()

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


def send_ukrnet_key(base_mail, base_mailpass, to_mail, akey):
    username = base_mail
    password = base_mailpass
    fromaddr = username
    toaddrs = to_mail

    txt = f"""
{to_mail}  
Для завершения регистрации и начала работы,
введите указанный код активации на сайте: {akey}
    
www.sharkevo.ru"""

    text_content = txt

    msg = EmailMessage()
    msg['Subject'] = 'The registration Sharkevo.ru'
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg.set_content(text_content)

    with smtplib.SMTP_SSL('smtp.ukr.net', 2525) as server:

        try:
            server.login(username, password)
            server.send_message(msg)
            logger.info('successfully sent the mail')

        except Exception as err:
            logger.info(str(err))

        finally:
            server.close()


if __name__ == '__main__':
    send_ukrnet_key('nsitala@ukr.net', 'fortuna-1', 'nsitala@gmail.com', '111')
