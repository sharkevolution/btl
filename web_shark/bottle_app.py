#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import logging
import json
import time
import pytz
import datetime
from collections import deque
from datetime import timedelta
from dateutil.tz import tzutc, tzlocal

import bottle
from bottle import route, run, request, static_file, default_app
from bottle import jinja2_template as template, redirect

# from gevent import monkey, pool; monkey.patch_all()
from waitress import serve

import config
import imexdata
import level7
import genpass

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def fruit_trsnsform(usdata, fruit):
    """
        Трансформация данных фигур и количества полученных от клиента в пригодный вид python

    :param usdata:
    :param fruit:
    :return:
    """

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

        self.tzutc = tzutc()    # При форм Даты определяет что будет Время в UTC
        self.tzlocal = tzlocal()  # При форм Даты определяет что будет Локальное время
        self.winter_summer = time.daylight  #Исп. ли переход на зимнее-летнее время
        #Время Unix в UTC формате
        self.__UNIX_EPOCH = datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.utc)
        self.complex_data = None

    def run(self):
        self.__year = self.complex_data[0]
        self.__month = self.complex_data[1]
        self.__day = self.complex_data[2]
        self.__hour = self.complex_data[3]
        self.__minute = self.complex_data[4]

        #Создаем локальное время
        naive = datetime.datetime(self.__year, self.__month, self.__day,
                                  self.__hour, self.__minute, tzinfo=tzlocal())

        #Переводим локальное время в UTC
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

    myfile = os.path.join(config.exm, 'FCNR.html')
    return template(myfile, private_code=gencode, zona=usdata.preload_figure)


@route('/lib/<filename>')
def server_lib(filename):
    fx = os.path.join(config.exm, 'lib')
    myfile = os.path.normpath(fx)

    return static_file(filename, root=myfile)


@route('/static/<filename>')
def server_static(filename):

    fx = os.path.join(config.exm, 'static')
    myfile = os.path.normpath(fx)
    return static_file(filename, root=myfile)


@route('/start')
@route('/upload_figure')
def redir_home():
    redirect('/')


@route('/<page>', method='POST')
def do_page(page):

    current_user = request.headers.get('host')
    gencode = request.forms.get('code')

    z = Pull.uname.keys()
    if not (gencode in list(z)):
        redirect('/')
    elif gencode not in Pull.uname:
        redirect('/')
    else:
        usdata = Pull.uname[gencode]

    if page == 'upload_figure':
        result = do_load()

    return result


@route('/result', method='GET')
def retresult():
    gencode = request.query.unique

    fx = os.path.join(config.exm, 'result')
    myfile = os.path.normpath(fx)

    filename = str(gencode) + '.xlsx'

    return static_file(filename, root=myfile, download=filename)



@route('/', method='GET')
def index():
    """ Главная точка входа на сайт

    :return:
    """

    gencode = genpass.generate_temp_password(15)  # Генератор уникального кода страницы
    current_host = request.headers.get('host')  # Запоминаем хост пользователя

    Pull.uname[gencode] = User()
    usdata = Pull.uname[gencode]
    usdata.current_host = current_host

    myfile = os.path.join(config.exm, 'FCNR.html')
    return template(myfile, private_code=gencode, zona=usdata.preload_figure)


def do_save(resdict, gencode):

    usdata = Pull.uname[gencode]
    fx = os.path.join(config.exm, 'result', gencode + '.xlsx')
    usdata.outfile = os.path.normpath(fx)

    if not os.path.exists(usdata.outfile):
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
        del(Tender.gencode_time[gencode])

    if gencode in Tender.waiting_line:
        Tender.waiting_line.remove(gencode)


@route('/getallitems.json', method='POST')
def shop_aj_getallitems():

    # https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Strict_mode
    # http://w-code.ru/jscript/ajax/ajax-xmlhttprequest

    json_data = request.forms.get('json_name')
    mydata = json.loads(json_data)

    gencode = mydata['unique']  # Получаем уникальный код сеанса пользователя
    subscribe = mydata['subscribe']  # Получаем статус подписки, 0 = подписано, 1 = отписаться
    fruit = mydata['fruit']  # Получаем массив в словаре с указанием кол-ва фигур и значений

    if subscribe == '1':
        # Отписаться от заявки
        subscribe = True
    elif subscribe == '0':
        # Подача заявки на подписку
        subscribe = False

    # Ответ пользователю в формате json
    optimization = {}
    optimization[1] = 'stop'

    if not gencode in Tender.gencode_time:
        # Запоминаем время нового сеанса пользователя
        Tender.gencode_time[gencode] = datetime.datetime.now()

    # Удаление сеансов превышающих порог времени ответа клиента
    for b, v in list(Tender.gencode_time.items()):
        differ = datetime.datetime.now() - v
        if differ.seconds > 10:
            # Время выхода на связь просрочено, удаляем сеанс пользователя
            if b in Pull.uname:
                del (Pull.uname[b])

            if b in Tender.gencode_time:
                del(Tender.gencode_time[b])

            if b in Tender.waiting_line:
                Tender.waiting_line.remove(b)

            if b == Tender.curr_optimize_gencode:
                # !!!Критическая секция!!!, остановка работающего потока
                level7.main_thread.stopping = True
                destroy_gencode(b)
                optimization[1] = 'stop'
                optimization[3] = 'Внимание, превышен порог времени ответа клиента, расчет сброшен!'

    if gencode in Tender.gencode_time:
        # Текущий Пользователь с нами, поэтому фиксируем время выхода его на связь
        Tender.gencode_time[gencode] = datetime.datetime.now()

        if not gencode in Tender.waiting_line:
            # Добавляем сеанс пользователя в очередь задач с учетом кол-ва макс подключений
            Tender.waiting_line.append(gencode)

        if level7.main_thread.flag_optimization is None:
            # Расчет в текущем времени не выполняется ни по одной заявке

            if gencode == Tender.waiting_line[0]:
                # Заявка в очереди совпадает с анализируемым текущим сеансом

                if subscribe:
                    # Пользователь отписался от выполнения заявки, необходимо изьять из очереди задач
                    destroy_gencode(gencode)
                    optimization[1] = 'stop'  # Флаг отказа оптимизации
                    optimization[3] = 'Вы, отписались от решения заявки!'
                else:
                    # Запуск расчета в отдельном потоке
                    if gencode in Pull.uname:
                        usdata = Pull.uname[gencode]

                        # Обработка в словаре fruit от клиента с данными фигур и количества
                        fruit_trsnsform(usdata, fruit)

                        onthr = level7.main_thread(usdata.pull_figure)
                        onthr.start()

                        Tender.curr_optimize_gencode = gencode  # Сохраняем инфр о коде пользователя в работе
                        optimization[1] = 'start'  # Флаг запуска оптимизации
                    else:
                        destroy_gencode(gencode)
                        optimization[1] = 'stop'  # Флаг отказа оптимизации
            else:
                if subscribe:
                    # Пользователь отписался от выполнения заявки, необходимо изьять заявку из очереди задач
                    destroy_gencode(gencode)
                    optimization[1] = 'stop'  # Флаг отказа оптимизации
                    optimization[3] = 'Вы, отписались от решения заявки!'
                else:
                    optimization[1] = 'wait'  # Флаг ожидания оптимизации

        elif level7.main_thread.flag_optimization == 'stop':
            # Поток отработал заявку

            if gencode == Tender.waiting_line[0]:
                # Заявка совпадает с анализируемым текущим сеансом

                # Сохраняем результат
                do_save(level7.main_thread.resdict, gencode)
                level7.main_thread.resdict = []
                level7.main_thread.flag_optimization = None

                gendel = Tender.waiting_line.popleft() # Удаляем отработаный сеанс после работы алгоритма
                Tender.curr_optimize_gencode = None

                optimization[1] = 'result'  # Флаг окончания оптимизации
                optimization[3] = 'Окончание работы алгоритма!'
            else:
                if subscribe:
                    # Пользователь отписался от выполнения заявки, необходимо изьять заявку из очереди задач
                    destroy_gencode(gencode)
                    optimization[1] = 'stop'  # Флаг отказа оптимизации
                    optimization[3] = 'Вы, отписались от решения заявки!'
                else:
                    optimization[1] = 'wait'  # Флаг ожидания оптимизации

        elif level7.main_thread.flag_optimization == 'start':
            if gencode == Tender.waiting_line[0]:

                if subscribe:
                    # !!!Критическая секция!!!, остановка работающего потока
                    level7.main_thread.stopping = True
                    destroy_gencode(gencode)
                    optimization[1] = 'stop'
                    optimization[3] = 'Вы, заявили об отказе подписки в процессе решения, поток остановлен!'
                else:
                    optimization[1] = 'start'  # Флаг запуска оптимизации
            else:
                if subscribe:
                    # Важно, необходимо удаление сеанса из очереди, пользователь отписался
                    destroy_gencode(gencode)
                    optimization[1] = 'stop'
                    optimization[3] = 'Вы, отписались от подписки!'
                else:
                    # Ограничиваем кол-во запросов ajax на подключение
                    if len(Tender.waiting_line) <= 5:
                        optimization[1] = 'wait'  # Флаг ожидания оптимизации
                    else:
                        destroy_gencode(gencode)
                        optimization[1] = 'stop'  # Флаг отказа оптимизации
                        optimization[3] = 'Превышено кол-во допустимых подключений'

        # Количество ожидающих пользователей
        optimization[2] = len(Tender.waiting_line)

        return json.dumps(optimization)
    else:
        return json.dumps(optimization)


def main_log():
    # myfile = os.path.join(config.exm, 'myapp.log')
    # logging.basicConfig(filename=myfile, level=logging.INFO, filemode='w')
    # logging.info('Started')

    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.info('start')


Unxtime = Epoch()
main_log()
Pull = Pull_user()

app = default_app()
# run(app, host='0.0.0.0', port=5000)
# bottle.run(server='gunicorn', host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True, workers=4)
# bottle.run(server='gevent', host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Waitress
# web: waitress-serve --port=$PORT cardisle.wsgi:application
serve(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
