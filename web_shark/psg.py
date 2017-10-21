#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import datetime
from datetime import timedelta

from psycopg2.extras import Json
from psycopg2 import sql
import psycopg2
from urllib.parse import urlparse

from web_shark import config
from web_shark import mail
from web_shark import genpass


def create_tables_two(connect_str):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS login_users (
            login_id SERIAL PRIMARY KEY,
            login_number VARCHAR(20) NOT NULL UNIQUE,
            login_password VARCHAR(20) NOT NULL,
            login_mail VARCHAR(50) NOT NULL,
            login_registration TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            login_status VARCHAR(3) NOT NULL,
            login_session VARCHAR(20) NOT NULL,
            login_lastdate TIMESTAMP WITHOUT TIME ZONE NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS access_users (
            access_id SERIAL PRIMARY KEY,
            access_name VARCHAR(50) NOT NULL,
            access_day INTEGER NOT NULL,
            access_price INTEGER NOT NULL,
            access_figures INTEGER NOT NULL,
            access_counts INTEGER NOT NULL,
            access_seconds INTEGER NOT NULL,
            access_longsession INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS billing_users (
            billing_id SERIAL PRIMARY KEY,
            login_id INTEGER NOT NULL,
            access_id INTEGER NOT NULL,
            FOREIGN KEY (login_id)
                REFERENCES login_users (login_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (access_id)
                REFERENCES access_users (access_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
             billing_promokey VARCHAR(8) NOT NULL,
             billing_start TIMESTAMP WITHOUT TIME ZONE,
             billing_end TIMESTAMP WITHOUT TIME ZONE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS figures_users (
            figures_id SERIAL PRIMARY KEY,
            billing_id INTEGER NOT NULL,
            FOREIGN KEY (billing_id)
                REFERENCES billing_users (billing_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            
            figures_pull json NOT NULL,
            
            figures_data_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            figures_data_end TIMESTAMP WITHOUT TIME ZONE,
            figures_result json,
            figures_permutation json,
            figures_matrix INTEGER,
            figures_knife INTEGER,
            figures_residue INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS admin (
            admin_id SERIAL PRIMARY KEY,
            admin_mail VARCHAR(50) NOT NULL,
            admin_mailpass VARCHAR(20) NOT NULL,
            admin_su VARCHAR(20) NOT NULL,
            admin_sms_login VARCHAR(20) NOT NULL,
            admin_sms_pass VARCHAR(20) NOT NULL
        )
        """
    )

    conn = None
    try:
        conn = psycopg2.connect(connect_str)
        cur = conn.cursor()

        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def access_create(connect_str):
    # Заполнение таблицы с уровнями доступа и стоимостью операций

    commands = (
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES({0}, 365, 0, 5, 20, 60, 300);
        """.format(config.access_name[0]),
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES({0}, 1, 150, 700, 700, 1800, 3600);
        """.format(config.access_name[1]),
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES({0}, 1, 150, 700, 700, 1800, 86400);
        """.format(config.access_name[2]),
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES({0}, 1, 150, 700, 700, 1800, 86400);
        """.format(config.access_name[3]),
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES({0}, 1, 150, 700, 700, 1800, 86400);
        """.format(config.access_name[4]),
    )

    conn = None
    try:
        conn = psycopg2.connect(connect_str)
        cur = conn.cursor()

        # create table one by one
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def new_user(connect_str):
    """
    Добавление в базу нового пользователя
    :param connect_str: 
    :return: 
    """

    commands = (
        """
        INSERT INTO login_users (login_number, login_password, login_mail, login_registration, login_status,
            login_session, login_lastdate)
            
            VALUES('380675691451', '8777', 'nsitala@gmail.com', '2017-06-24 04:05:06', 'on', 'xxx', 
                '2017-06-24 04:05:06');
        """,)

    conn = None
    try:
        conn = psycopg2.connect(connect_str)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if error.pgcode == '23505':
            print('Указанный номер телефона есть в базе')
    finally:
        if conn is not None:
            conn.close()


def new_user_two(connect_str, form_email, form_pass, loggin_session):
    """
    Добавление в базу нового пользователя
    :param connect_str:
    :return:
    """

    quote = "\'"
    em = quote + form_email + quote
    ps = quote + form_pass + quote
    ks = quote + loggin_session + quote
    f = "%Y-%m-%d %H:%M:%S"
    dt = datetime.datetime.utcnow()
    dtf = quote + dt.strftime(f) + quote

    err = 0
    conn = None
    try:
        if config.heroku:
            url = urlparse(os.environ["USERS_DB_URL"])
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port)
        else:
            conn = psycopg2.connect(config.connect_base)

        cur = conn.cursor()
        qw = """SELECT * FROM login_users WHERE login_mail = {0};""".format(em)
        cur.execute(qw)
        log_user = cur.fetchone()

        if log_user:

            lg = quote + str(log_user[0]) + quote

            cur.execute("""UPDATE login_users 
                            SET login_password = {0}, 
                                login_session = {1},
                                login_lastdate = {2}
                            WHERE login_id = {3};""".format(ps, ks, dtf, lg))
            conn.commit()

        else:

            qw = """INSERT INTO login_users (login_number, login_password, login_mail, 
                                        login_registration, login_status, 
                                        login_session, login_lastdate)
        
                    VALUES('None', {0}, {1}, {2}, 'on', {3}, {4});
                """.format(ps, em, dtf, ks, dtf)

            cur.execute(qw)
            conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        # print(error)
        err = 'error insert base'
    finally:
        if conn is not None:
            conn.close()
        return err


def new_billing(connect_str):
    """ Добавление в базу тарифа и срока действия тарифа
    
    :param connect_str: 
    :return: 
    """

    conn = None
    try:
        conn = psycopg2.connect(connect_str)
        cur = conn.cursor()

        cur.execute("""SELECT login_id FROM login_users
                        WHERE login_number = '380675691451'; """)

        idlogin = cur.fetchone()
        print(idlogin[0])

        cur.execute("""SELECT access_id FROM access_users
                        WHERE access_name = {0}; """.format(config.access_name[0]))

        idacc = cur.fetchone()
        print(idacc[0])

        cur.execute("""INSERT INTO billing_users (login_id, access_id, billing_promokey, 
                        billing_start, billing_end) values ({0}, {1}, '7777', 
                        '2017-06-24 04:05:06', 
                        '2017-06-24 04:05:06'); """.format(idlogin[0], idacc[0]))

        cur.execute("""INSERT INTO billing_users (login_id, access_id, billing_promokey)
                        values ({0}, {1}, '8888'); """.format(idlogin[0], idacc[0]))

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def figures_add(connect_str):
    # Сохранение пула фигур выбранных пользователем

    conn = None
    try:
        conn = psycopg2.connect(connect_str)
        cur = conn.cursor()

        my = {'pull': [[1, 0], [2, 0]]}

        cur.execute("""INSERT INTO figures_users (billing_id, figures_pull, figures_data_start)
                        values ({0}, {1}, '2017-06-24 04:05:06'); """.format(1, Json(my)))

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_admin():
    conn = None
    try:
        if config.heroku:
            url = urlparse(os.environ["USERS_DB_URL"])
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port)
        else:
            conn = psycopg2.connect(config.connect_base)

        cur = conn.cursor()
        cur.execute("""INSERT INTO admin (admin_mail, admin_mailpass, 
                        admin_su, admin_sms_login, admin_sms_pass)
                        values ({0}, {1}, {2}, {3}, {4}); """.format("'nsitala@gmail.com'",
                                                                     "'sonic1980'",
                                                                     "'zzz'",
                                                                     "'zzz'",
                                                                     "'zzz'"))

        # cur.execute("""INSERT INTO admin (admin_mail, admin_mailpass, admin_su)
        #                 values ('nsitala@gmail.com', 'sonic1980', 'zzz'); """)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def find_regigistration(logemail, logpass):
    logger = config.main_log()
    login_data = None
    conn = None

    try:

        if config.heroku:
            url = urlparse(os.environ["USERS_DB_URL"])

            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        else:
            conn = psycopg2.connect(config.connect_base)

        cur = conn.cursor()

        quote = "\'"
        logemail = quote + logemail + quote
        logpass = quote + logpass + quote

        qw = """SELECT * FROM login_users
                    WHERE login_mail = {0} AND login_password = {1};""".format(logemail, logpass)

        cur.execute(qw)
        login_data = cur.fetchone()

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(error)
    finally:
        if conn is not None:
            conn.close()

            return login_data


def get_admin_email():
    logger = config.main_log()
    base_mail = None
    base_mailpass = None

    try:
        if config.heroku:
            url = urlparse(os.environ["USERS_DB_URL"])
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port)
        else:
            conn = psycopg2.connect(config.connect_base)

        cur = conn.cursor()
        cur.execute("""SELECT admin_mail, admin_mailpass FROM admin;""")

        admin_data = cur.fetchone()
        if admin_data:
            base_mail = admin_data[0]
            base_mailpass = admin_data[1]

        # cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(error)
    finally:
        if conn is not None:
            conn.close()

        return base_mail, base_mailpass


def get_billing_users(form_phone, form_pass, curr_key):
    """
        Поиск зарегистрированного пользователя и разрешенных доступов
    :return:
    """
    logger = config.main_log()
    conn = None
    bill_data = None
    data = find_regigistration(form_phone, form_pass)
    if data:

        try:
            if config.heroku:

                url = urlparse(os.environ["USERS_DB_URL"])

                conn = psycopg2.connect(
                    database=url.path[1:],
                    user=url.username,
                    password=url.password,
                    host=url.hostname,
                    port=url.port
                )
            else:
                conn = psycopg2.connect(config.connect_base)

            cur = conn.cursor()
            login_id = data[0]

            quote = "\'"
            bilqwery = login_id
            qkey = quote + curr_key + quote

            qw = """SELECT * FROM billing_users
                        WHERE login_id = {0} AND billing_promokey = {1};""".format(bilqwery, qkey)

            cur.execute(qw)
            bill_data = cur.fetchall()
            logger.info(bill_data)

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.info(error)
        finally:
            if conn is not None:
                conn.close()

    return bill_data


def check_active_billing(username, promokey):
    """
        Проверка активного промо-кода и активация нового кода
        при наличии неактивированного кода

    :return:
    """
    logger = config.main_log()
    login_data = None
    conn = None

    get_promo = {'date_start': None, 'date_end': None,
                 'tarif': None, 'status': 'нет'}

    try:
        if config.heroku:
            url = urlparse(os.environ["USERS_DB_URL"])
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        else:
            conn = psycopg2.connect(config.connect_base)

        cur = conn.cursor()
        quote = "\'"
        login_user = quote + username + quote

        # Проверка существования пользователя
        qw = """SELECT * FROM login_users
                    WHERE login_mail = {0};""".format(login_user)

        cur.execute(qw)
        user = cur.fetchone()

        f = "%Y-%m-%d %H:%M:%S"
        dt = datetime.datetime.utcnow()
        d = timedelta(days=+1)
        dt1 = dt + d
        dtnow = quote + dt.strftime(f) + quote
        dtafter = quote + dt1.strftime(f) + quote
        promokey2 = quote + promokey + quote

        if user:
            login_id = user[0]

            # Делаем выборку для определения есть ли действующий сейчас промокод
            qw = """SELECT * FROM billing_users
                        WHERE login_id = {0}
                        AND billing_start < timestamp {1}
                        AND billing_end > timestamp {1};""".format(login_id, dtnow)
            cur.execute(qw)
            current_key = cur.fetchone()

            if current_key:

                access_id = quote + str(current_key[2]) + quote
                qw = """SELECT * FROM access_users
                            WHERE access_id = {0};""".format(access_id)
                cur.execute(qw)
                access_name = cur.fetchone()
                if access_name:
                    get_promo['date_start'] = str(current_key[4])
                    get_promo['date_end'] = str(current_key[5])
                    get_promo['tarif'] = str(access_name[1])
                    get_promo['status'] = 'Активно'

            else:

                qw = """SELECT * FROM billing_users
                            WHERE login_id = {0}
                            AND billing_start IS NULL
                            AND billing_promokey = {1};""".format(login_id, promokey2)
                cur.execute(qw)
                empty_key = cur.fetchone()
                if empty_key:
                    id = quote + str(empty_key[0]) + quote
                    # Активация нового промокода
                    cur.execute("""UPDATE billing_users SET billing_start = {0}, billing_end = {1} WHERE
                                        billing_id = {2};""".format(dtnow, dtafter, id))

                    access_id = quote + str(empty_key[2]) + quote
                    qw = """SELECT * FROM access_users
                                WHERE access_id = {0};""".format(access_id)
                    cur.execute(qw)
                    access_name = cur.fetchone()

                    if access_name:
                        get_promo['date_start'] = str(dtnow.strip(quote))
                        get_promo['date_end'] = str(dtafter.strip(quote))
                        get_promo['tarif'] = str(access_name[1])
                        get_promo['status'] = 'Активно'
                else:

                    name = quote + config.access_name[0] + quote
                    qw = """SELECT * FROM access_users
                                WHERE access_name = {0};""".format(name)
                    cur.execute(qw)
                    access_name = cur.fetchone()
                    if access_name:
                        get_promo['date_start'] = str(dtnow.strip(quote))
                        get_promo['date_end'] = str(dtnow.strip(quote))
                        get_promo['tarif'] = name.strip(quote)
                        get_promo['status'] = 'Активно'

        else:

            name = quote + config.access_name[0] + quote
            qw = """SELECT * FROM access_users
                        WHERE access_name = {0};""".format(name)
            cur.execute(qw)
            access_name = cur.fetchone()
            if access_name:
                get_promo['date_start'] = str(dtnow.strip(quote))
                get_promo['date_end'] = str(dtnow.strip(quote))
                get_promo['tarif'] = name.strip(quote)
                get_promo['status'] = 'Активно'


        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(error)
    finally:
        if conn is not None:
            conn.close()

    return get_promo


def create_unused_promokey(mail, access_id, count):
    # Создание новых свободных(неиспользованных) кодов для будущей активации

    logger = config.main_log()
    login_data = None
    conn = None

    try:
        if config.heroku:
            url = urlparse(os.environ["USERS_DB_URL"])
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port)
        else:
            # connect_base = "dbname='mylocaldb' user='postgres' host='localhost' password='sitala'"
            # config.update_connect(connect_base)

            conn = psycopg2.connect(config.connect_base)

        cur = conn.cursor()

        quote = "\'"
        login_mail = quote + mail + quote

        qw = """SELECT * FROM login_users
                    WHERE login_mail = {0};""".format(login_mail)

        cur.execute(qw)
        user = cur.fetchone()
        if user:
            login_id = user[0]

            for b in range(count):
                newpromokey = genpass.generate_temp_password(4)
                promokey = quote + newpromokey + quote

                # Вставка нового промокода неактивного
                cur.execute("""INSERT INTO billing_users (login_id, access_id, billing_promokey)
                                values ({0}, {1}, {2}); """.format(login_id, access_id, promokey))

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(error)
    finally:
        if conn is not None:
            conn.close()

            return login_data


if __name__ == '__main__':
    # create_tables_two()

    # http://postgresql.ru.net/manual/ddl-constraints.html
    # http://eax.me/postgresql-install/

    connect_base = "dbname='mylocaldb' user='postgres' host='localhost' password='sitala'"
    config.update_connect(connect_base)

    # insert_admin()
    # base_mail, base_mailpass = get_admin_email()
    # mail.send_mail(base_mail, base_mailpass, base_mail)

    create_unused_promokey(mail="nsitala@gmail.com", access_id=466, count=4)
    # check_active_billing(username="YdgPNH8HHQYoC7g")
