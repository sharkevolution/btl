#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests

def send_sms(sms_login, sms_pass):
    # Отправка сообщения пользователю
    login = sms_login  # phone number
    password = sms_pass  # Password
    alphaName = 'gsm1'  # string, sender id (alpha-name)

    abonent = '380732218247'
    text = 'sharkevo: started calculation'

    xml = "<?xml version='1.0' encoding='utf-8'?><request_sendsms><username><![CDATA[" + \
          login + "]]></username><password><![CDATA[" + password + "]]></password><from><![CDATA[" + \
          alphaName + "]]></from><to><![CDATA[" + abonent + "]]></to><text><![CDATA[" + \
          text + "]]></text></request_sendsms>"

    url = 'https://gate.smsclub.mobi/xml/'
    headers = {'Content-type': 'text/xml; charset=utf-8'}

    try:
        res = requests.post(url, data=xml, headers=headers)
    except:
        pass
        # print(res.status_code)
        # print(res.raise_for_status())