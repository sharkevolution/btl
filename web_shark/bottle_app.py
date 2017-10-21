#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import logging
# from logging.handlers import RotatingFileHandler

import json
import time
import pytz
import re
import datetime
from collections import deque
from datetime import timedelta
from dateutil.tz import tzutc, tzlocal

import requests

import bottle
from bottle import route, run, request, static_file, hook, default_app
from bottle import jinja2_template as template, redirect, response

# from gevent import monkey, pool; monkey.patch_all()
# from waitress import serve
import cherrypy
import wsgigzip

from web_shark import config
from web_shark import imexdata
from web_shark import level7
from web_shark import genpass
from web_shark import psg
from web_shark import mail

# from web_shark import perfomance

import psycopg2
from urllib.parse import urlparse

# import dropbox
#
# dbx = dropbox.Dropbox('3XLapBh9QeAAAAAAAAAAGaqI8f2xBwQNwX4pxksBTCQFXDWR6OV5zXgZgkj1XIeK')
# nn = dbx.users_get_current_account()
# print(nn)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def html_navigation():

    navigation = [
        '<li class="pushy-link"><a href="/login">Авторизация</a></li>',
        '<li class="pushy-link"><a href="/">Результаты</a></li>',
        '<li class="pushy-link"><a href="/mystory">Обо мне</a></li>',
        '<li class="pushy-link"><a href="/">На главную</a></li>'
    ]

    return navigation


def fruit_trsnsform(usdata, fruit):
    """
        Трансформация данных фигур и количества полученных от клиента в пригодный вид python

    :param usdata:
    :param fruit:
    :return:
    """
    usdata.pull_figure = []

    for b, v in list(fruit.items()):
        usdata.pull_figure.append([int(v['f']), int(v['c'])])


class Tender():
    """ Создание очереди решения задач заданных пользователями

    """
    gencode_time = {}
    waiting_line = deque([])
    curr_optimize_gencode = None


class Pull_user(object):
    def __init__(self):
        self.uname = {}


class User(object):
    def __init__(self):
        self.preload_figure = []  # Предварительный список загруженный из файла
        self.pull_figure = []  # Список фигур и количества под профилем пользователя
        self.impfile = None  # Путь сохранения импортируемого файла
        self.outfile = None  # Путь сохранения файла с результатом расчета
        self.current_host = None  # Запоминаем хост пользователя
        self.online_export = False
        self.account = None
        self.flag_promokey = None  # Показывает состояние выполнения активации временного ключа


def authenticated(func):
    """ Проверка авторизации пользователя
    
    :param func: 
    :return: 
    """

    def wrapped(*args, **kwargs):

        # Проверяем печеньку есть ли она и срок действия
        us = request.get_cookie("account", secret='some-secret-key')
        usdict = json.loads(us)
        username = usdict['login_password']

        if username == 'sharkx3':
            return func(*args, **kwargs)
        else:
            redirect('/login')

    return wrapped


def redirect_https(func):
    """ Проверка авторизации пользователя
    """

    def wrapped(*args, **kwargs):

        try:
            heroku = urlparse(os.environ["CHERRY"])

        except Exception as ex:

            heroku = 0

        if heroku:

            if not request.url.startswith('https'):

                url = request.url.replace('http://', 'https://', 1)
                code = 301

                return redirect(url, code=code)
            else:
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapped


@route('/yandex_1b8eabd36008dc04.html', method='GET')
def yandex():
    myfile = os.path.join(config.exm, 'yandex_1b8eabd36008dc04.html')
    return template(myfile)


@route('/google20b85008b048860b.html', method='GET')
def google():
    myfile = os.path.join(config.exm, 'google20b85008b048860b.html')
    return template(myfile)


@route('/robots.txt', method='GET')
def robots():
    """robot.txt, для того что-б поисковики индексировали все"""
    return 'User-agent: *\nDisallow:\nHost: www.sharkevo.ru\n\n'


@route('/sitemap.xml', method='GET')
def sitemap():
    """XML-файл с информацией для поисковых систем
        (таких как Яндекс, Google, Bing, Поиск@Mail.Ru)
        о страницах веб-сайта, которые подлежат индексации."""

    tm = datetime.datetime.now() - timedelta(days=1)
    curtime = tm.strftime("%Y-%m-%d")
    cur = ['myform', 'story']
    res = []
    for r in cur:
        res.append([r, curtime])

    fx = os.path.join(config.exm, 'sitemap')

    return template(fx, res=res, curtime=curtime)


class Epoch():
    """ Расчет времени в Unix (сначала передаваемое время переводится в Локальное,
        Форматируем локал время в UTC и вычисляем время секунд, после передаем
        время в секундах UTC как результат
    """

    def __init__(self):
        self.tzutc = tzutc()  # При форм Даты определяет что будет Время в UTC
        self.tzlocal = tzlocal()  # При форм Даты определяет что будет Локальное время
        self.winter_summer = time.daylight  # Исп. ли переход на зимнее-летнее время
        # Время Unix в UTC формате
        self.__UNIX_EPOCH = datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.utc)
        self.complex_data = None

    def run(self):
        self.__year = self.complex_data[0]
        self.__month = self.complex_data[1]
        self.__day = self.complex_data[2]
        self.__hour = self.complex_data[3]
        self.__minute = self.complex_data[4]

        # Создаем локальное время
        naive = datetime.datetime(self.__year, self.__month, self.__day,
                                  self.__hour, self.__minute, tzinfo=tzlocal())

        # Переводим локальное время в UTC
        self.utc_datetime = naive.astimezone(pytz.utc)

        self.delta = self.utc_datetime - self.__UNIX_EPOCH
        self.seconds = self.delta.total_seconds()
        self.ms = self.seconds * 1000

        return self.seconds


def do_load():
    current_user = request.headers.get('host')
    gencode = request.forms.get('code')
    usdata = Pull.uname[gencode]

    data = request.files.get('fkml')
    data_path = os.path.join(config.exm, 'analiz_data', data.filename)

    if not data_path:
        redirect('/')

    if not os.path.exists(data_path):
        data.save(data_path)
    else:
        os.remove(data_path)
        data.save(data_path)

    new_path_dir = os.path.dirname(__file__)
    new_path_data = os.path.join(new_path_dir, data_path)
    new_path_figure = os.path.normpath(new_path_data)
    usdata.impfile = new_path_figure

    # Изменить загрузку из файла в preload
    usdata.preload_figure = imexdata.dispatcher_extension(new_path_figure, 'data')

    # response.set_cookie("account", 'shark', secret='some-secret-key')
    myfile = os.path.join(config.exm, 'FCNR.html')
    navigation = html_navigation()

    return template(myfile, private_code=gencode,
                    zona=usdata.preload_figure,
                    navigation=navigation,
                    current_user='Гость')


@route('/<name>/<filename>')
def server_static(name, filename):
    fx = os.path.join(config.exm, name)
    myfile = os.path.normpath(fx)
    return static_file(filename, root=myfile)


@route('/start')
@route('/upload_figure')
# @authenticated
def redir_home():
    redirect('/')


@route('/mystory', method='GET')
def my_story():
    myfile = os.path.join(config.exm, 'mypage.html')
    return template(myfile)


@route('/registration', method='POST')
def do_registration():
    current_user = request.headers.get('host')
    form_email = request.forms.get('email')
    form_pass = request.forms.get('pass')
    form_reg = request.forms.get('me_submit')

    # response.set_cookie("account", 'shark', secret='some-secret-key')
    if form_reg == 'registration':

        akey = genpass.generate_temp_password(6)

        base_mail, base_mailpass = psg.get_admin_email()
        logger.info(base_mail)
        logger.info(base_mailpass)

        mail.send_mail_key(base_mail, base_mailpass, form_email, akey)

        us = json.dumps({'email': form_email,
                         'pass': form_pass,
                         'akey': akey})
        response.set_cookie("registry_sharkevo", us, secret='some-secret-key')
        myfile = os.path.join(config.exm, 'regmail.html')

        return template(myfile, register_answer="")

    elif form_reg == 'login':

        # Проверка электронного адреса
        # addressToVerify = 'info@emailhippo.com'
        # match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

        # if match == None:
        #     print('Bad Syntax')
        #     raise ValueError('Bad Syntax')
        login_data = psg.find_regigistration(form_email, form_pass)

        if login_data:
            us = json.dumps({'login_email': form_email})
            response.set_cookie("account", us, secret='some-secret-key')
            redirect('/')

        else:
            myfile = os.path.join(config.exm, 'login.html')

    return template(myfile)


@route('/open', method='POST')
def do_open():

    akey = request.forms.get('pass')

    us = request.get_cookie("registry_sharkevo", secret='some-secret-key')
    usdict = json.loads(us)
    form_akey = usdict['akey']
    form_email = usdict['email']
    form_pass = usdict['pass']

    if akey == form_akey:

        # Уникальный код сессии пользователя
        loggin_session = genpass.generate_temp_password(15)
        ret = psg.new_user_two(config.connect_base, form_email, form_pass, loggin_session)
        if ret is 0:

            psg.create_unused_promokey(mail=form_email, access_id=466, count=5)

            us = json.dumps({'login_email': form_email,
                             'login_pass': form_pass})
            response.set_cookie("account", us, secret='some-secret-key')
            redirect('/')
        else:
            myfile = os.path.join(config.exm, 'regmail.html')
            return template(myfile, registry_answer="Ошибка активации, пользователь уже существует!!")
    else:
        myfile = os.path.join(config.exm, 'regmail.html')
        return template(myfile, registry_answer="Ошибка активации, неверный код!!")



@route('/admin', method='POST')
def do_admin():
    json_data = request.forms.get('json_file')
    mydata = json.loads(json_data)
    secret_letter = mydata['params']  # Получаем уникальный код сеанса пользователя
    if secret_letter:
        # Устанавливаем админскую куку
        response.set_cookie("admin_level", 'blue', secret='some-secret-key')


@route('/login', method='GET')  # or @route('/login', method='POST')
def do_auth():
    myfile = os.path.join(config.exm, 'login.html')
    return template(myfile)


@route('/upload_figure', method='POST')
def do_page():
    current_user = request.headers.get('host')
    gencode = request.forms.get('code')

    z = Pull.uname.keys()
    if not (gencode in list(z)):
        redirect('/')
    elif gencode not in Pull.uname:
        redirect('/')
    else:
        usdata = Pull.uname[gencode]

        result = do_load()

    return result


@route('/result', method='GET')
def retresult():
    gencode = request.query.unique

    fx = os.path.join(config.exm, 'result')
    myfile = os.path.normpath(fx)

    filename = str(gencode) + '.xlsx'

    return static_file(filename, root=myfile, download=filename)


@route('/develop', method='GET')
def do_develop():
    devpass = request.get_cookie("admin_level", secret='some-secret-key')
    if devpass == 'blue':
        return 'ok'
    else:
        return 'bad'


@route('/', method='GET')
# @redirect_https
def index():
    """ Главная точка входа на сайт

    :return:
    """

    gencode = genpass.generate_temp_password(15)  # Генератор уникального кода страницы
    current_host = request.headers.get('host')  # Запоминаем хост пользователя

    Pull.uname[gencode] = User()
    usdata = Pull.uname[gencode]
    usdata.current_host = current_host

    # expire_date = datetime.datetime.now()
    # expire_date = expire_date + datetime.timedelta(days=2)
    current_user = 'Гость'
    # Проверка на активность профиля пользователя

    get_promo = psg.check_active_billing(current_user, '1')

    us = request.get_cookie("account", secret='some-secret-key')

    try:
        usdict = json.loads(us)
        form_user = usdict['login_email']
        form_pass = usdict['login_pass']

        get_promo = psg.check_active_billing(form_user, '1')

        login_data = psg.find_regigistration(form_user, form_pass)
        if login_data:
            current_user = form_user
        else:
            current_user = 'Гость'

    except Exception as ex:
        username = None

    # usdata.account = username

    # response.set_cookie("account", 'sharkx', secret='some-secret-key', expires=expire_date)
    devpass = request.get_cookie("admin_level", secret='some-secret-key')

    myfile = os.path.join(config.exm, 'FCNR.html')

    navigation = html_navigation()
    if devpass == 'blue':
        navigation.extend(['<li class="pushy-link"><a href="/develop">Админ</a></li>'])

    return template(myfile, private_code=gencode,
                    zona=usdata.preload_figure,
                    navigation=navigation,
                    current_user=current_user,
                    arrkey=get_promo)


def do_save(resdict, gencode):
    usdata = Pull.uname[gencode]
    fx = os.path.join(config.exm, 'result', gencode + '.xlsx')
    usdata.outfile = os.path.normpath(fx)

    if not os.path.exists(usdata.outfile):
        logging.info(resdict)
        imexdata.saveExcel(resdict, usdata.outfile)
    else:
        os.remove(usdata.outfile)
        imexdata.saveExcel(resdict, usdata.outfile)

    return 0


def destroy_gencode(gencode):
    # Принудительное удаление сеанса из очереди
    if gencode in Pull.uname:
        del (Pull.uname[gencode])

    if gencode in Tender.gencode_time:
        del (Tender.gencode_time[gencode])

    if gencode in Tender.waiting_line:
        Tender.waiting_line.remove(gencode)


def destroy_gencode_waiting(gencode):
    if gencode in Tender.waiting_line:
        Tender.waiting_line.remove(gencode)


@route('/promokey.json', method='POST')
def promokey():
    """ Активатор ключа введенного пользователем

    :return:
    """

    json_data = request.forms.get('json_file')
    mydata = json.loads(json_data)

    promokey = mydata['promokey']
    gencode = mydata['unique']
    usdata = Pull.uname[gencode]

    # !!! Написать проверку наличия свободного промоключа и запись в базу
    # Проверяем печеньку есть ли она и срок действия
    us = request.get_cookie("account", secret='some-secret-key')

    try:
        usdict = json.loads(us)
        # username = usdict['login_password']
        username = usdict['login_email']
    except Exception as ex:
        username = None

    get_promo = psg.check_active_billing(username, promokey)

    # if usdata.flag_promokey:
    #     pass
    # else:
    #     usdata.flag_promokey = True

    return json.dumps({'prop': 'stop', 'arr': get_promo})


@route('/checkpromo.json', method='POST')
def check_promokey():
    """ Проверка активности промоключа для проведения расчета

    """
    json_data = request.forms.get('json_file')
    mydata = json.loads(json_data)

    gencode = mydata['unique']  # Получаем уникальный код сеанса пользователя
    usdata = Pull.uname[gencode]
    us = request.get_cookie("account", secret='some-secret-key')

    try:
        usdict = json.loads(us)
        form_user = usdict['login_email']
        form_pass = usdict['login_pass']
        get_promo = psg.check_active_billing(form_user, '1')

        response.set_cookie("access_sharkevo", json.dumps(get_promo), secret='some-secret-key')

    except Exception:
        pass

    if usdata.flag_promokey:
        pass
    else:
        usdata.flag_promokey = True

    return json.dumps({1: 'activated_key'})


@route('/feedback.json', method='POST')
def feedback():
    json_data = request.forms.get('json_file')
    mydata = json.loads(json_data)

    data = mydata['exp']  # Получаем уникальный код сеанса пользователя
    gencode = mydata['unique']
    usdata = Pull.uname[gencode]

    fx = os.path.join(config.exm, 'result')
    path = os.path.normpath(fx)
    myfile = os.path.join(path, 'temp_shk.xlsx')

    if usdata.online_export:
        pass
    else:
        imexdata.export_excel(data, myfile)
        usdata.online_export = True

    return json.dumps({1: 'prepared_file'})


@route('/export', method='GET')
def export():
    gencode = request.query.unique
    usdata = Pull.uname[gencode]
    usdata.online_export = False

    fx = os.path.join(config.exm, 'result')
    myfile = os.path.normpath(fx)

    filename = 'temp_shk.xlsx'

    return static_file(filename, root=myfile, download=filename)


@route('/getallitems.json', method='POST')
def shop_aj_getallitems():
    # https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Strict_mode
    # http://w-code.ru/jscript/ajax/ajax-xmlhttprequest

    json_data = request.forms.get('json_name')
    mydata = json.loads(json_data)

    gencode = mydata['unique']  # Получаем уникальный код сеанса пользователя
    subscribe = mydata['subscribe']  # Получаем статус подписки, 0 = подписано, 1 = отписаться
    fruit = mydata['fruit']  # Получаем массив в словаре с указанием кол-ва фигур и значений
    knox = mydata['knox']
    limright = mydata['limright']
    site_attempt = mydata['attempt']
    develop = mydata['correto']
    if not develop:
        develop = [4]

    # print(knox, limright)

    if subscribe == '1':
        # Отписаться от заявки
        subscribe = True
    elif subscribe == '0':
        # Подача заявки на подписку
        subscribe = False

    # Готовим ответ пользователю в формате json
    optimization = {}
    optimization[1] = 'stop'  # Начальное значение оптимизации
    optimization[4] = 0  # Процент выполнения
    optimization[3] = ''  # Информация для клиента
    optimization[5] = ''  # Номер пользователя в списке

    if not gencode in Tender.gencode_time:
        # Запоминаем время нового сеанса пользователя
        Tender.gencode_time[gencode] = datetime.datetime.now()
        # print('init gencode')

    # Удаление сеансов превышающих порог времени ответа клиента
    for b, v in list(Tender.gencode_time.items()):
        differ = datetime.datetime.now() - v

        if differ.seconds > 3600:
            # Клиент отсутствует более 1ч, удаляем как мусор
            if b in Pull.uname:
                del (Pull.uname[b])

            if b in Tender.gencode_time:
                del (Tender.gencode_time[b])

        if not b == Tender.curr_optimize_gencode:
            if differ.seconds > 15:
                # Потеря активного соединения, удаляем окончательно пользователя
                if b in Tender.waiting_line:
                    Tender.waiting_line.remove(b)

        if b == Tender.curr_optimize_gencode:
            if differ.seconds > 3600:
                # !!!Критическая секция!!!, остановка работающего потока
                level7.main_thread.stopping = True
                level7.main_thread.flag_optimization = None
                level7.main_thread.progress = 0
                destroy_gencode_waiting(b)
                optimization[1] = 'stop'
                optimization[3] = 'Превышен лимит ответа, расчет сброшен!'

    # Проверяем печеньку есть ли она и срок действия
    us = request.get_cookie("access_sharkevo", secret='some-secret-key')

    try:
        get_promo = json.loads(us)
    except Exception as ex:
        optimization[1] = 'stop'
        optimization[3] = 'Неавторизованный доступ!'
        optimization[2] = ''
        optimization[5] = ''
        return json.dumps(optimization)

    if get_promo['tarif'] == config.access_name[0]:
        optimization[1] = 'stop'
        optimization[3] = 'Неавторизованный доступ!'
        optimization[2] = ''
        optimization[5] = ''
        return json.dumps(optimization)

    else:
        f = "%Y-%m-%d %H:%M:%S"
        dt = datetime.datetime.utcnow()
        dtnow = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

        begin_time = get_promo['date_start']
        begin_time1 = datetime.datetime.strptime(begin_time, f)

        end_time = get_promo['date_end']
        end_time1 = datetime.datetime.strptime(end_time, f)

        if not (dtnow >= begin_time1 and dtnow <= end_time1):
            optimization[1] = 'stop'
            optimization[3] = 'Неавторизованный доступ!'
            optimization[2] = ''
            optimization[5] = ''
            return json.dumps(optimization)
        else:

            if gencode in Tender.gencode_time:
                # Текущий Пользователь с нами, поэтому фиксируем время выхода его на связь
                Tender.gencode_time[gencode] = datetime.datetime.now()
                # print('fixe time gencode')

                if gencode in Tender.waiting_line:
                    # Запись процента выполнения расчета
                    if gencode == Tender.waiting_line[0]:
                        optimization[4] = level7.main_thread.progress
                    else:
                        optimization[4] = 0
                else:
                    # Добавляем сеанс пользователя в очередь задач с учетом кол-ва макс подключений
                    Tender.waiting_line.append(gencode)
                    # Добавление в профиль пользовтаеля фигур и количества при старте подписки
                    usdata = Pull.uname[gencode]

                    fruit_trsnsform(usdata, fruit)
                    optimization[4] = 0

                if level7.main_thread.flag_optimization is None:
                    # Расчет в текущем времени не выполняется ни по одной заявке

                    if gencode == Tender.waiting_line[0]:
                        # Заявка в очереди совпадает с анализируемым текущим сеансом

                        if subscribe:
                            # Пользователь отписался от выполнения заявки, необходимо изьять из очереди задач
                            destroy_gencode_waiting(gencode)
                            optimization[1] = 'stop'  # Флаг отказа оптимизации
                            optimization[3] = 'Вы, отписались от решения заявки!'
                            Tender.curr_optimize_gencode = None
                        else:
                            # Запуск расчета в отдельном потоке
                            if gencode in Pull.uname:
                                usdata = Pull.uname[gencode]

                                level7.main_thread.progress = 0
                                if usdata.pull_figure:
                                    # Есть фигуры для решения

                                    # # Работа в одном процессе (блокирующий режим)
                                    # onthr = level7.main_thread_two(usdata.pull_figure, int(knox), int(limright),
                                    #                                int(site_attempt), develop)
                                    # onthr.run()

                                    # Работа в отдельном процессе системы (многопоточный режим)
                                    onthr = level7.main_thread(usdata.pull_figure, int(knox), int(limright),
                                                               int(site_attempt), develop)
                                    onthr.start()

                                    Tender.curr_optimize_gencode = gencode  # Сохраняем инфр о коде пользователя в работе
                                    optimization[1] = 'start'  # Флаг запуска оптимизации
                                else:
                                    destroy_gencode_waiting(gencode)
                                    optimization[1] = 'stop'  # Флаг отказа оптимизации
                                    optimization[3] = 'Нет данных, нажмите повторно Старт!'
                            else:
                                destroy_gencode(gencode)
                                optimization[1] = 'stop'  # Флаг отказа оптимизации
                                optimization[3] = 'Разрыв соединения, обновите страницу!'
                    else:
                        if subscribe:
                            # Пользователь отписался от выполнения заявки, необходимо изьять заявку из очереди задач
                            destroy_gencode_waiting(gencode)
                            optimization[1] = 'stop'  # Флаг отказа оптимизации
                            optimization[3] = 'Вы, отписались от решения заявки!'
                        else:
                            optimization[1] = 'wait'  # Флаг ожидания оптимизации

                elif level7.main_thread.flag_optimization == 'stop':
                    # Поток отработал заявку

                    if gencode == Tender.waiting_line[0]:
                        # Заявка совпадает с анализируемым текущим сеансом

                        # Сохраняем результат
                        if level7.main_thread.resdict:
                            do_save(level7.main_thread.resdict, gencode)
                            optimization[1] = 'result'
                            optimization[3] = 'Окончание работы алгоритма!'
                        # else:
                        #     optimization[3] = 'Решение ранее сброшено, перезагрузите страницу'
                        #     optimization[1] = 'stop'

                        level7.main_thread.resdict = []
                        level7.main_thread.flag_optimization = None
                        level7.main_thread.progress = 0

                        gendel = Tender.waiting_line.popleft()  # Удаляем отработаный сеанс после работы алгоритма
                        Tender.curr_optimize_gencode = None

                    else:
                        if subscribe:
                            # Пользователь отписался от выполнения заявки, необходимо изьять заявку из очереди задач
                            destroy_gencode_waiting(gencode)
                            optimization[1] = 'stop'  # Флаг отказа оптимизации
                            optimization[3] = 'Вы, отписались от решения заявки!'
                        else:
                            optimization[1] = 'wait'  # Флаг ожидания оптимизации

                elif level7.main_thread.flag_optimization == 'start':
                    if gencode == Tender.waiting_line[0]:

                        if subscribe:
                            # !!!Критическая секция!!!, остановка работающего потока
                            level7.main_thread.stopping = True
                            level7.main_thread.progress = 0
                            level7.main_thread.flag_optimization = None
                            destroy_gencode_waiting(gencode)
                            optimization[1] = 'stop'
                            optimization[3] = 'Вы, остановили поток решения!'
                            Tender.curr_optimize_gencode = None
                        else:
                            optimization[1] = 'start'  # Флаг запуска оптимизации
                    else:
                        if subscribe:
                            # Важно, необходимо удаление сеанса из очереди, пользователь отписался
                            destroy_gencode_waiting(gencode)
                            optimization[1] = 'stop'
                            optimization[3] = 'Вы, отказались от подписки!'
                        else:
                            # Ограничиваем кол-во запросов ajax на подключение
                            if len(Tender.waiting_line) <= 5:
                                optimization[1] = 'wait'  # Флаг ожидания оптимизации
                            else:
                                destroy_gencode_waiting(gencode)
                                optimization[1] = 'stop'  # Флаг отказа оптимизации
                                optimization[3] = 'Превышен лимит подключений: {0}'.format(5)

                elif level7.main_thread.flag_optimization == 'error':
                    if gencode == Tender.waiting_line[0]:
                        optimization[1] = 'stop'
                        optimization[3] = 'Критическая ошибка, обновите страницу!'
                        level7.main_thread.stopping = True
                        level7.main_thread.progress = 0
                        Tender.curr_optimize_gencode = None

                        destroy_gencode_waiting(gencode)
                        level7.main_thread.flag_optimization = None

                # Количество ожидающих пользователей
                if gencode in Tender.waiting_line:
                    optimization[2] = len(Tender.waiting_line)
                    optimization[5] = Tender.waiting_line.index(gencode)
                else:
                    optimization[2] = ''
                    optimization[5] = ''

                # print(optimization)

                return json.dumps(optimization)
            else:
                return json.dumps(optimization)


# @hook('before_request')
# def beforeRequest():
#
#     try:
#         heroku = urlparse(os.environ["CHERRY"])
#
#     except Exception as ex:
#
#         heroku = 0
#
#     if heroku:
#
#         if not request.url.startswith('https'):
#             return redirect(request.url.replace('http', 'https', 1))


# @hook('before_request')
# def strip_path():
#     username = request.get_cookie("account", secret='some-secret-key')
#     if username:
#         pass
#     else:
#         redirect('/registration')


# def main_log():
#     level = logging.INFO
#
#     file_handler = RotatingFileHandler('ex/microblog.log', 'a', 1 * 1024 * 1024, 10)
#     file_handler.setLevel(logging.INFO)
#     file_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
#
#     logger = logging.getLogger('info')
#     logger.addHandler(file_handler)
#     logger.setLevel(level)  # even if not required...
#
#     return logger


def send_sms():
    # Отправка сообщения пользователю
    login = '380732218247'  # phone number
    password = 'tgxm8ou'  # Password
    alphaName = 'gsm1'  # string, sender id (alpha-name)

    abonent = '380963786850'
    text = 'Sending SMS from SMSCLUB via python'

    xml = "<?xml version='1.0' encoding='utf-8'?><request_sendsms><username><![CDATA[" + \
          login + "]]></username><password><![CDATA[" + password + "]]></password><from><![CDATA[" + \
          alphaName + "]]></from><to><![CDATA[" + abonent + "]]></to><text><![CDATA[" + \
          text + "]]></text></request_sendsms>"

    url = 'https://gate.smsclub.mobi/xml/'
    headers = {'Content-type': 'text/xml; charset=utf-8'}
    res = requests.post(url, data=xml, headers=headers)
    print(res.status_code)
    print(res.raise_for_status())


logger = config.main_log()
logger.info('hello')

Unxtime = Epoch()
Pull = Pull_user()

#
# command = """
#         SELECT relname, pg_class.relkind as relkind FROM pg_class, pg_namespace
#             WHERE pg_class.relnamespace=pg_namespace.oid
#                 AND pg_class.relkind IN ('v', 'r')
#                 AND pg_namespace.nspname='my_schema'
#                 AND relname = 'my_table';
# """
#
#
# new_table =  """
#         CREATE TABLE vendors (
#             vendor_id SERIAL PRIMARY KEY,
#             vendor_name VARCHAR(255) NOT NULL
#         )
#         """
#
#
#
# logger.info('logging test' + str(con))


# app = default_app()
# run(app, host='0.0.0.0', port=5000, debug=True)
# bottle.run(server='gunicorn', host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True, workers=4)
# bottle.run(server='gevent', host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# Waitress
# web: waitress-serve --port=$PORT cardisle.wsgi:application
# serve(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


try:
    heroku_flag = urlparse(os.environ["CHERRY"])
    logger.info(heroku_flag)
except Exception as ex:

    heroku_flag = None

config.update_heroku(heroku_flag)

if config.heroku:

    url = urlparse(os.environ["USERS_DB_URL"])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    # urlparse.uses_netloc.append("postgres")
    # url = urlparse(os.environ["USERS_DB_URL"])

    # conn = psycopg2.connect(
    #     database=url.path[1:],
    #     user=url.username,
    #     password=url.password,
    #     host=url.hostname,
    #     port=url.port
    # )

    connect_base = "dbname={0}, user={1}, password={2}, host={3}, port={4}".format(dbname,
                                                                                   user,
                                                                                   password,
                                                                                   host,
                                                                                   port)
    logger.info('test------------------------------')
    logger.info(connect_base)
    logger.info('test_end ------------------------------')
    config.update_connect(connect_base)

    # psg.create_tables_two(config.connect_str)


    app = wsgigzip.GzipMiddleware(bottle.default_app())

    cherrypy.config.update({'server.socket_host': "0.0.0.0",
                            'server.socket_port': int(os.environ.get("PORT", 5000))})
    cherrypy.tree.graft(app)
    cherrypy.engine.start()
    cherrypy.engine.block()

else:

    try:
        # connect_base = "dbname='mylocaldb' user='postgres' host='localhost' password='sitala'"
        config.update_connect(config.connect_base)

        # psg.create_tables_two(config.connect_str)
        # psg.access_create(config.connect_str)
        # psg.new_user(config.connect_str)
        # psg.new_billing(config.connect_str)
        # psg.figures_add(config.connect_str)

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    # send_sms()  # Отправка СМС с промокодом

    app = default_app()
    run(app, host='0.0.0.0', port=5000, debug=True)

# http://www.williammalone.com/articles/create-html5-canvas-javascript-sprite-animation/
