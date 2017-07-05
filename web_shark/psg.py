#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from psycopg2.extras import Json
from psycopg2 import sql
import psycopg2
from urllib.parse import urlparse

from web_shark import config
from web_shark import mail

def create_tables_two(connect_str):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS login_users (
            login_id SERIAL PRIMARY KEY,
            login_number VARCHAR(20) NOT NULL UNIQUE,
            login_password VARCHAR(20) NOT NULL,
            login_mail VARCHAR(50) NOT NULL,
            login_registration TIMESTAMP WITH TIME ZONE NOT NULL,
            login_status VARCHAR(3) NOT NULL,
            login_session VARCHAR(20) NOT NULL,
            login_lastdate TIMESTAMP WITH TIME ZONE NOT NULL
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
             billing_start TIMESTAMP WITH TIME ZONE NOT NULL,
             billing_end TIMESTAMP WITH TIME ZONE NOT NULL
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
            
            figures_data_start TIMESTAMP WITH TIME ZONE NOT NULL,
            figures_data_end TIMESTAMP WITH TIME ZONE,
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
            admin_su VARCHAR(20) NOT NULL
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
            VALUES('Демо', 365, 0, 5, 20, 60, 300);
        """,
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES('1 день', 1, 150, 700, 700, 1800, 3600);
        """,
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES('1 день', 1, 150, 700, 700, 1800, 86400);
        """,
        """
        INSERT INTO access_users (access_name, access_day, access_price, access_figures, access_counts,
            access_seconds, access_longsession)
            VALUES('1 день', 1, 150, 700, 700, 1800, 86400);
        """,
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
                        WHERE access_name = 'Демо'; """)

        idacc = cur.fetchone()
        print(idacc[0])

        cur.execute("""INSERT INTO billing_users (login_id, access_id, billing_promokey, billing_start, billing_end)
                        values ({0}, {1}, '7777', '2017-06-24 04:05:06', '2017-06-24 04:05:06'); """.format(idlogin[0],
                                                                                                           idacc[0]))

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
        conn = psycopg2.connect(config.connect_str)
        cur = conn.cursor()

        cur.execute("""INSERT INTO admin (admin_mail, admin_mailpass, admin_su)
                        values ({0}, {1}, {2}); """.format("'nsitala@gmail.com'", "'sonic1980'", "'zzz'"))

        # cur.execute("""INSERT INTO admin (admin_mail, admin_mailpass, admin_su)
        #                 values ('nsitala@gmail.com', 'sonic1980', 'zzz'); """)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def find_regigistration(logphone, logpass):
    login_data = None
    conn = None
    try:

        url = urlparse(os.environ["USERS_DB_URL"])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        # connect_base = "dbname='mylocaldb' user='postgres' host='localhost' password='sitala'"
        # config.update_connect(connect_base)

        # conn = psycopg2.connect(config.connect_str)
        cur = conn.cursor()

        quote = "\'"
        logphone = quote + logphone + quote
        logpass = quote + logpass + quote

        qw = """SELECT * FROM login_users
                    WHERE login_number = {0} AND login_password = {1};""".format(logphone, logpass)

        cur.execute(qw)
        login_data = cur.fetchone()

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

            return login_data




def get_admin_email():

    base_mail = None
    base_mailpass = None

    conn = None
    try:

        conn = psycopg2.connect(config.connect_str)
        cur = conn.cursor()

        cur.execute("""SELECT admin_mail, admin_mailpass FROM admin
                        WHERE admin_id = 1; """)

        admin_data = cur.fetchone()
        base_mail = admin_data[0]
        base_mailpass = admin_data[1]

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        return base_mail, base_mailpass



if __name__ == '__main__':
    # create_tables_two()

    # http://postgresql.ru.net/manual/ddl-constraints.html
    # http://eax.me/postgresql-install/

    connect_base = "dbname='mylocaldb' user='postgres' host='localhost' password='sitala'"
    config.update_connect(connect_base)

    insert_admin()
    base_mail, base_mailpass = get_admin_email()
    mail.send_mail(base_mail, base_mailpass, base_mail)


