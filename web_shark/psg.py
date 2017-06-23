#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import psycopg2

def create_tables_two(connect_str):
      """ create tables in the PostgreSQL database"""
      commands = (
            """
            CREATE TABLE IF NOT EXISTS login_users (
                login_id SERIAL PRIMARY KEY,
                login_number VARCHAR(20) NOT NULL,
                login_password VARCHAR(8) NOT NULL,
                login_registration TIMESTAMP WITH TIME ZONE NOT NULL,
                login_status VARCHAR(3) NOT NULL
            )
            """,
            """ CREATE TABLE IF NOT EXISTS access_users (
                    access_id SERIAL PRIMARY KEY,
                    access_name VARCHAR(50) NOT NULL,
                    access_day INTEGER NOT NULL,
                    access_price INTEGER NOT NULL
                    )
            """,
            """
            CREATE TABLE IF NOT EXISTS billing_users (
                    login_id INTEGER NOT NULL,
                    access_id INTEGER NOT NULL,
                    PRIMARY KEY (login_id , access_id),
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
            """)
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


if __name__ == '__main__':
      create_tables_two()

      # http://postgresql.ru.net/manual/ddl-constraints.html
      # http://eax.me/postgresql-install/


